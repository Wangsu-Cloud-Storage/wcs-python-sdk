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
from wcs.commons.util import urlsafe_base64_encode

from wcs.services.uploadprogressrecorder import UploadProgressRecorder

mkblk_retries = Config.mkblk_retries
bput_retries = Config.bput_retries
mkfile_retries = Config.mkfile_retries
concurrency = Config.concurrency

class MultipartUpload(object):
    
    def __init__(self,url):
        self.url = url
        self.token = ''
        self.path = ''
        self.size = 0
        self.key = ''
        self.params = ''
        self.recorder = UploadProgressRecorder()
        self.blocknum = 0
        self.results = []
        self.uploadBatch = ''
        self.progress = 0

    def __need_retry(self,code):
        if code == 500:
            return True
        return False

    def _define_config(self,path,token,params):
        self.token = token
        self.path = path
        self.size = os.path.getsize(self.path)
        self.key = os.path.basename(path)
        self.params = params
        self.blocknum = int(self.size/Config.block_size + 1)
        self.results = []
        self.uploadBatch = 'Null'
        self.progress = 0
        self.modify_time = time.time() 

    def _record_upload_progress(self, result, size):
        result_dict = dict(zip(['offset', 'code', 'ctx'], result))
        result_dict['size'] = size
        record_data = self.recorder.get_upload_record(self.key)
        record_data['upload_record'].append(result_dict)
        if result_dict['code'] == 200:
            self.progress += size
            debug('Current block size: %d, total upload size: %d' % (int(size), self.progress))
        self.recorder.set_upload_record(self.key, record_data)

    def _records_parse(self):
        records = self.recorder.get_upload_record(self.key)
        debug(records)
        offsetlist = [i * (Config.block_size) for i in range(0,self.blocknum)]
        if records:
            self.uploadBatch = records['uploadBatch']
            self.results = records['upload_record']
            for record in self.results:
                if record['code'] == 200:
                    offsetlist.remove(record['offset'])
                    blockid = record['offset']/Config.block_size
                    if blockid < self.blocknum - 1:
                        self.progress += Config.block_size
                    else:              
                        self.progress += self.size - (blockid * Config.block_size)       
        return offsetlist
    
    def _make_bput_post(self, ctx, bputnum, bput_next):
        url = self.__bput_url(ctx, bputnum*Config.bput_size)
        headers = self.__generate_headers()
        return _post(url=url, headers=headers, data=bput_next)

    def __bput_url(self, ctx, offset):
        return '{0}/bput/{1}/{2}'.format(self.url, ctx, offset)

    def __block_url(self,size,blocknum):
        return '{0}/mkblk/{1}/{2}'.format(self.url, size, int(blocknum))

    def __file_url(self):
        url = ['{0}/mkfile/{1}'.format(self.url, self.size)]
        if self.params:
            for k, v in self.params.items():
                url.append('x:{0}/{1}'.format(k, urlsafe_base64_encode(v)))
        url = '/'.join(url)
        return url

    def __generate_headers(self):
        headers = {'Authorization':self.token}
        headers['uploadBatch'] = self.uploadBatch
        return headers

    def _mlk_url(self, offset):
        blockid = offset/Config.block_size
        if blockid < self.blocknum - 1:
            size = Config.block_size
        else:
            size = int(self.size - (blockid * Config.block_size))
        return self.__block_url(int(size), blockid), size

    def _make_block(self, offset):
        url,size = self._mlk_url(offset)
        headers = self.__generate_headers()        
        with open(self.path, 'rb') as f:
            bput = readfile(f, offset, Config.bput_size)
            blkcode, blktext = _post(url=url,headers=headers, data=bput)
            #while mkblk_retries and self.__need_retry(blkcode):
            #    blkcode, blktext = _post(url=url, headers=headers, data=bput)
            #    mkblk_retries -= 1
            if blkcode != 200:
                result = [offset, blkcode, blktext['message']]
            else:
                result = self._make_bput(f, blktext['ctx'], offset)
        with record_lock:
            self._record_upload_progress(result,size)
    
    def _make_bput(self, f, ctx, offset):
        bputnum = 1
        offset_next = offset + Config.bput_size
        bput_next = readfile(f, offset_next, Config.bput_size)
        bputcode = 200
        bputtext = {'ctx' : ctx}
        while bput_next and bputnum < Config.block_size/Config.bput_size:
            bputcode, bputtext = self._make_bput_post(ctx, bputnum, bput_next)
            #while bput_retries and self.__need_retry(bputcode):
            #    bputcode, bputtext = self._make_bput_post(ctx, bputnum, bput_next)
            #    bput_retries -= 1
            if bputcode != 200:
                return offset, bputcode, bputtext['message']
            ctx = bputtext['ctx']
            offset_next = offset + bputtext['offset']
            bput_next = readfile(f, offset_next, Config.bput_size)
            bputnum += 1
        return offset, bputcode, bputtext['ctx']
 
    def _is_complete(self):
        self.results = self.recorder.get_upload_record(self.key)
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
        for offset in [i * (Config.block_size) for i in range(0,self.blocknum)]:
            for result in self.results['upload_record']:
                if offset == result['offset']:
                    blkstatus.append(result['ctx'])
        return blkstatus

    def _make_file(self):
        blkstatus = self._get_blkstatus()
        url = self.__file_url()
        body = ','.join(blkstatus)
        headers = self.__generate_headers()
        code,text = _post(url=url,headers=headers,data=body)
        #while mkfile_retries and self.__need_retry(code):
        #    code,text = _post(url=url,headers=headers,data=body)
        #    retry -= 1
        self.recorder.delete_upload_record(self.key)
        return code,text

    def _initial_records(self):
        self.uploadBatch = GetUuid()
        records = {'uploadBatch':self.uploadBatch}
        records['modify_time'] = time.time() 
        records['upload_record'] = []
        self.recorder.set_upload_record(self.key,records)

    def upload(self,path,token,params):
        debug('File %s multipart upload start!' % (path))
        self._define_config(path,token,params)
        offsets = self._records_parse()
        debug('Uncomplete offsetlist: %s, uploadid: %s, complete size: %d' % (offsets, self.uploadBatch,self.progress))
        if len(offsets) != 0:
            debug('Thare are %d offsets need to upload' % (len(offsets)))
            if self.uploadBatch == 'Null':
                self._initial_records()
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
            debug('Sorry, These block %s upload fail, more details please see %s' % (fail_list, logging_folder)) 
            raise Exception("Multipart upload fail")

