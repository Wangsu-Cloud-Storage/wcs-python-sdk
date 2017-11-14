import os
import time
import requests
import threading
from threading import Thread
from multiprocessing.dummy import Pool as ThreadPool 

from wcs.commons.config import Config
from wcs.commons.http import _post
from wcs.commons.logme import debug,error
from wcs.commons.util import readfile,file_to_stream,GetUuid
from wcs.commons.util import urlsafe_base64_encode,https_check

from wcs.services.uploadprogressrecorder import UploadProgressRecorder

concurrency = int(Config.concurrency)
block_size = int(Config.block_size)
bput_size = int(Config.bput_size)

class MultipartUpload(object):
    
    def __init__(self,url):
        self.url = url
        self.token = ''
        self.path = ''
        self.size = 0
        self.key = ''
        self.recorder = UploadProgressRecorder()
        self.blocknum = 0
        self.results = []
        self.uploadBatch = ''
        self.progress = 0

    def __need_retry(self,code):
        if code == 500:
            return True
        return False

    def _define_config(self,path,token,upload_id=None):
        self.token = token
        self.path = path
        self.size = os.path.getsize(self.path)
        self.key = os.path.basename(path)
        if self.size % block_size != 0:
            self.blocknum = int(self.size/block_size + 1)
        else:
            self.blocknum = int(self.size/block_size)
        self.results = []
        self.uploadBatch = upload_id or ''
        self.progress = 0
        self.modify_time = time.time() 

    def _record_upload_progress(self, result, size):
        result_dict = dict(zip(['offset', 'code', 'ctx'], result))
        result_dict['size'] = size
        record_data = self.recorder.get_upload_record(self.uploadBatch)
        offset = -1
        for res in record_data['upload_record']:
            if res['offset'] == result_dict['offset']:
                offset = res['offset']
                res['code'] = result_dict['code']
                res['ctx'] = result_dict['ctx']
        if offset == -1:
            record_data['upload_record'].append(result_dict)
        if result_dict['code'] == 200:
            self.progress += size
            debug('Current block size: %d, total upload size: %d' % (int(size), self.progress))
        self.recorder.set_upload_record(self.uploadBatch, record_data)

    def _records_parse(self, upload_id):
        records = self.recorder.get_upload_record(upload_id)
        debug(records)
        offsetlist = [i * (block_size) for i in range(0,self.blocknum)]
        if records:
            self.uploadBatch = records['uploadBatch']
            self.results = records['upload_record']
            for record in self.results:
                if record['code'] == 200:
                    offsetlist.remove(record['offset'])
                    blockid = record['offset']/block_size
                    if blockid < self.blocknum - 1:
                        self.progress += block_size
                    else:              
                        self.progress += self.size - (blockid * block_size)       
        return offsetlist
    
    def _make_bput_post(self, ctx, bputnum, bput_next):
        url = https_check(self.__bput_url(ctx, bputnum*bput_size))
        headers = self.__generate_headers()
        return _post(url=url, headers=headers, data=bput_next)

    def __bput_url(self, ctx, offset):
        return '{0}/bput/{1}/{2}'.format(self.url, ctx, offset)

    def __block_url(self,size,blocknum):
        return '{0}/mkblk/{1}/{2}'.format(self.url, size, int(blocknum))

    def __file_url(self):
        url = ['{0}/mkfile/{1}'.format(self.url, self.size)]
        #if self.params:
        #    for k, v in self.params.items():
        #        url.append('x:{0}/{1}'.format(k, urlsafe_base64_encode(v)))
        url = '/'.join(url)
        return url

    def __generate_headers(self):
        headers = {'Authorization':self.token}
        headers['uploadBatch'] = self.uploadBatch
        return headers

    def _mlk_url(self, offset):
        blockid = offset/block_size
        if blockid < self.blocknum - 1:
            size = block_size
        else:
            size = int(self.size - (blockid * block_size))
        return self.__block_url(int(size), blockid), size

    def _make_block(self, offset):
        url,size = self._mlk_url(offset)
        url = https_check(url)
        headers = self.__generate_headers()        
        mkblk_retries = int(Config.mkblk_retries)
        with open(self.path, 'rb') as f:
            bput = readfile(f, offset, bput_size)
            blkcode, blktext,_ = _post(url=url,headers=headers, data=bput)
            while mkblk_retries and self.__need_retry(blkcode):
                blkcode, blktext,_ = _post(url=url, headers=headers, data=bput)
                mkblk_retries -= 1
            if blkcode != 200:
                result = [offset, blkcode, blktext['message']]
            else:
                result = self._make_bput(f, blktext['ctx'], offset)
        self._record_upload_progress(result,size)
    
    def _make_bput(self, f, ctx, offset):
        bputnum = 1
        offset_next = offset + bput_size
        bput_next = readfile(f, offset_next, bput_size)
        bputcode = 200
        bputtext = {'ctx' : ctx}
        bput_retries = int(Config.bput_retries)
        while bput_next and bputnum < block_size/bput_size:
            bputcode, bputtext, _ = self._make_bput_post(ctx, bputnum, bput_next)
            while bput_retries and self.__need_retry(bputcode):
                bputcode, bputtext, _ = self._make_bput_post(ctx, bputnum, bput_next)
                bput_retries -= 1
            if bputcode != 200:
                return offset, bputcode, bputtext['message']
            ctx = bputtext['ctx']
            offset_next = offset + bputtext['offset']
            bput_next = readfile(f, offset_next, bput_size)
            bputnum += 1
        return offset, bputcode, bputtext['ctx']
 
    def _is_complete(self):
        self.results = self.recorder.get_upload_record(self.uploadBatch)
        debug(self.results)
        if len(self.results['upload_record']) < self.blocknum:
            return 0
        for result in self.results['upload_record']:
            if result['code'] != 200:
                return 0
        return 1

    def _get_failoffsets(self):
        offsetlist = [i *  int(Config.block_size) for i in range(0, self.blocknum)]
        if self.results:
            for result in self.results['upload_record']:
                if result['offset'] in offsetlist:
                    offsetlist.remove(result['offset'])
        return offsetlist
        
    def _get_blkstatus(self):
        blkstatus = []
        for offset in [i * (block_size) for i in range(0,self.blocknum)]:
            for result in self.results['upload_record']:
                if offset == result['offset']:
                    blkstatus.append(result['ctx'])
        return blkstatus

    def _make_file(self):
        mkfile_retries = int(Config.mkfile_retries)
        blkstatus = self._get_blkstatus()
        url = https_check(self.__file_url())
        body = ','.join(blkstatus)
        headers = self.__generate_headers()
        code,text,logid = _post(url=url,headers=headers,data=body)
        while mkfile_retries and self.__need_retry(code):
            code,text,logid = _post(url=url,headers=headers,data=body)
            retry -= 1
        self.recorder.delete_upload_record(self.uploadBatch)
        return code,text,logid

    def _initial_records(self):
        self.uploadBatch = GetUuid()
        records = {'uploadBatch':self.uploadBatch}
        records['modify_time'] = time.time() 
        records['upload_record'] = []
        self.recorder.set_upload_record(self.uploadBatch,records)

    def upload(self,path,token,upload_id=None):
        self._define_config(path,token,upload_id)
        if upload_id:
            self.recorder.find_upload_record(upload_id)
            offsets = self._records_parse(upload_id)
            debug('Uncomplete offsetlist: %s, uploadid: %s, complete size: %d' % (offsets, upload_id, self.progress))

        else:
            debug("Now start a new multipart upload task")
            self._initial_records()
            offsets = [i * (block_size) for i in range(0,self.blocknum)]

        if len(offsets) != 0:
            debug('Thare are %d offsets need to upload' % (len(offsets)))
            debug('Now start upload file blocks') 
            pool = ThreadPool(concurrency)
            pool.map(self._make_block, offsets)
            pool.close()
            pool.join()

        if self._is_complete():
            debug('Now all blocks have upload suc.')
            return self._make_file()
        else:
            fail_list = self._get_failoffsets() 
            upload_record = str(Config.tmp_record_folder) + self.uploadBatch
            debug('Sorry! Mulitpart upload fail,more detail see %s' % upload_record) 
            raise Exception("Multipart upload fail")

