#!/usr/bin/python
## -*- coding: utf-8 -*-

import os
import sys
import time
from multiprocessing import Lock
from multiprocessing.dummy import Pool as ThreadPool
from os.path import expanduser
from wcs.commons.config import Config
from wcs.commons.http import _post
from wcs.commons.logme import debug,warning,error
from wcs.commons.util import https_check
from wcs.commons.util import readfile,GetUuid
from wcs.services.uploadprogressrecorder import UploadProgressRecorder
from wcs.commons.error_deal import WcsSeriveError

#config_file = os.path.join(expanduser("~"), ".wcscfg")

lock = Lock()

class MultipartUpload(object):
    """分片上传类
    分片上传引入了块和片，一个文件由一到多个块组成，而每个块由一到多个片组成，块大小和片大小是可配的。块之间可以并发上传也可以顺序上传，块内的片之间只能顺序上传
    分片上传通过导入UploadProgressRecorder实现断点续传
    Attributes:
        url: 上传域名
        token: 鉴权token
        path: 源文件路径
        size: 源文件大小
        key: 源文件名
        blocknum: 源文件块数目
        results: 读取上传进度到这个变量
        uploadBatch: upload id
        progress: 当前上传进度
        recorder: UploadProgressRecorder的实例
        cfg: Config的实例
        concurrency: 块并发度
        block_size: 块大小
        bput_size: 片大小
        
    """   
    def __init__(self,url):
        self.url = url
        self.token = ''
        self.path = ''
        self.size = 0
        self.key = ''
        self.blocknum = 0
        self.results = []
        self.uploadBatch = ''
        self.progress = 0
        self.recorder = None
        #self.cfg = Config(config_file)
        self.cfg = Config()
        try:
            self.concurrency = int(self.cfg.concurrency)
            self.block_size = int(self.cfg.block_size)
            self.bput_size = int(self.cfg.bput_size)
        except ValueError as e:
            error(u"Invalid value,please check .wcscfg file")
            sys.exit()
            

    def __need_retry(self,code):
        if code == 500 or code == -1:
            return True
        return False

    def _define_config(self,path,token,upload_id=None):
        self.token = token
        self.path = path
        self.size = os.path.getsize(self.path)
        self.key = os.path.basename(path)
        if self.size % self.block_size != 0:
            self.blocknum = int(self.size/self.block_size + 1)
        else:
            self.blocknum = int(self.size/self.block_size)
        self.results = []
        self.uploadBatch = upload_id or ''
        self.progress = 0
        self.modify_time = time.time() 

    def _record_upload_progress(self, result, size):
        result_dict = dict(zip(['offset', 'code', 'ctx'], result))
        result_dict['size'] = size
        if result_dict['code'] == 200:
            lock.acquire()
            self.progress += size
            debug('Current block size: %d, total upload size: %d' % (int(size), self.progress))
            lock.release()
        self.recorder.set_upload_record(result_dict['offset'],result_dict)

    def _records_parse(self, upload_id):
        records = self.recorder.get_upload_record()
        offsetlist = [i * (self.block_size) for i in range(0,self.blocknum)]
        debug(records)
        if records:
            self.uploadBatch = records['uploadBatch']
            self.results = records['upload_record']
            for record in self.results:
                try:
                    record = eval(record)
                except SyntaxError as e:
                    debug('Get ctx/offset fail,error ctx/offset:{0}'.format(record))

                except Exception as exc_e:
                    debug('Get ctx/offset fail,errorinfo:{0}'.format(exc_e))

                if record['code'] == 200:
                    offsetlist.remove(record['offset'])
                    blockid = record['offset']/self.block_size
                    if blockid < self.blocknum - 1:
                        self.progress += self.block_size
                    else:              
                        self.progress += self.size - (blockid * self.block_size)       
        return offsetlist
    
    def _make_bput_post(self, ctx, bputnum, bput_next):
        url = https_check(self.__bput_url(ctx, bputnum*self.bput_size))
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
        try:
            if int(self.cfg.traffic_limit):
                headers['x-wos-traffic-limit'] = '{0}'.format(self.cfg.traffic_limit)
        except Exception as e:
            raise ValueError('traffic_limit parameter configuration error：{0}'.format(self.cfg.traffic_limit))
        return headers

    def _mlk_url(self, offset):
        blockid = offset/self.block_size
        if blockid < self.blocknum - 1:
            size = self.block_size
        else:
            size = int(self.size - (blockid * self.block_size))
        return self.__block_url(int(size), blockid), size

    def _make_block(self, offset):
        url,size = self._mlk_url(offset)
        url = https_check(url)
        headers = self.__generate_headers()        
        try:
            mkblk_retries = int(self.cfg.mkblk_retries)
        except ValueError as e:
            warning('parameter mkblk_retries is invalid, so use default value 3')
            mkblk_retries = 3
        with open(self.path, 'rb') as f:
            bput = readfile(f, offset, self.bput_size)
            blkcode, blktext,_ = _post(url=url,headers=headers, data=bput)
            while mkblk_retries and self.__need_retry(blkcode):
                blkcode, blktext,_ = _post(url=url, headers=headers, data=bput)
                mkblk_retries -= 1
            if blkcode != 200:
                result = [offset, blkcode, blktext['message']]
                debug('make block fail,code :{0},message :{1}'.format(blkcode, blktext))
            else:
                result = self._make_bput(f, blktext['ctx'], offset)
        self._record_upload_progress(result,size)
        return blkcode
    
    def _make_bput(self, f, ctx, offset):
        bputnum = 1
        offset_next = offset + self.bput_size
        bput_next = readfile(f, offset_next, self.bput_size)
        bputcode = 200
        bputtext = {'ctx' : ctx}
        try:
            bput_retries = int(self.cfg.bput_retries)
        except ValueError as e:
            warning('parameter bput_retries is invalid, so use default value 3')
            bput_retries = 3
        while bput_next and bputnum < self.block_size/self.bput_size:
            bputcode, bputtext, _ = self._make_bput_post(ctx, bputnum, bput_next)
            while bput_retries and self.__need_retry(bputcode):
                bputcode, bputtext, _ = self._make_bput_post(ctx, bputnum, bput_next)
                bput_retries -= 1
            if bputcode != 200:
                return offset, bputcode, bputtext['message']
            ctx = bputtext['ctx']
            offset_next = offset + bputtext['offset']
            bput_next = readfile(f, offset_next, self.bput_size)
            bputnum += 1
        return offset, bputcode, bputtext['ctx']
 
    def _is_complete(self):
        self.results = self.recorder.get_upload_record()
        debug(self.results)
        if len(self.results['upload_record']) < self.blocknum:
            return 0
        for result in self.results['upload_record']:
            result = eval(result)
            if result['code'] != 200:
                return 0
        return 1

    def _get_failoffsets(self):
        offsetlist = [i *  int(self.block_size) for i in range(0, self.blocknum)]
        if self.results:
            for result in self.results['upload_record']:
                result = eval(result)
                if result['offset'] in offsetlist:
                    offsetlist.remove(result['offset'])
        return offsetlist
        
    def _get_blkstatus(self):
        blkstatus = []
        for offset in [i * (self.block_size) for i in range(0,self.blocknum)]:
            for result in self.results['upload_record']:
                result = eval(result)
                if offset == result['offset']:
                    blkstatus.append(result['ctx'])
        return blkstatus

    def _make_file(self):
        try:
            mkfile_retries = int(self.cfg.mkfile_retries)
        except ValueError as e:
            warning(u"parameter mkfile_retries is invalid, so use default value 3")
            mkfile_retries = 3
        blkstatus = self._get_blkstatus()
        url = https_check(self.__file_url())
        body = ','.join(blkstatus)
        headers = self.__generate_headers()
        code,text,logid = _post(url=url,headers=headers,data=body)
        while mkfile_retries and self.__need_retry(code):
            code,text,logid = _post(url=url,headers=headers,data=body)
            mkfile_retries -= 1
        self.recorder.delete_upload_record()
        return code,text,logid

    def _initial_records(self):
        self.uploadBatch = GetUuid()
        debug('New upload id: %s' % self.uploadBatch)
        self.recorder = UploadProgressRecorder(self.uploadBatch)

    def upload(self,path,token,upload_id=None):
        self._define_config(path,token,upload_id)
        if upload_id:
            self.recorder = UploadProgressRecorder(upload_id)
            offsets = self._records_parse(upload_id)
            debug('Uncomplete offsetlist: %s, uploadid: %s, complete size: %d' % (offsets, upload_id, self.progress))

        else:
            debug("Now start a new multipart upload task")
            self._initial_records()
            offsets = [i * (self.block_size) for i in range(0,self.blocknum)]

        if len(offsets) != 0:
            debug('There are %d offsets need to upload' % (len(offsets)))
            debug('Now start upload file blocks') 
            if self.concurrency > 0:
                pool = ThreadPool(self.concurrency)
                pool.map(self._make_block, offsets)
                pool.close()
                pool.join()

            elif self.concurrency == 0:
                for offset in offsets:
                    return_code = self._make_block(offset)
                    if 400 <= int(return_code) <= 499:
                        debug('Single-Thread,attempt authentication failed,exit the task.')
                        sys.exit()
            else:
                raise ValueError('Invalid concurrency')
                sys.exit()

        if self._is_complete():
            debug('Now all blocks have upload suc.')
            return self._make_file()
        else:
            fail_list = self._get_failoffsets() 
            upload_record = str(Config.tmp_record_folder) + self.uploadBatch
            debug('Sorry! Mulitpart upload fail,more detail see %s' % upload_record)
            return self.results
            #raise Exception("Multipart upload fail")

    def smart_upload(self,path,token,upload_id=None):
        self._define_config(path,token,upload_id)
        if upload_id:
            self.recorder = UploadProgressRecorder(upload_id)
            offsets = self._records_parse(upload_id)
            debug('Uncomplete offsetlist: %s, uploadid: %s, complete size: %d' % (offsets, upload_id, self.progress))

        else:
            debug("Now start a new multipart upload task")
            self._initial_records()
            offsets = [i * (self.block_size) for i in range(0,self.blocknum)]

        if len(offsets) != 0:
            debug('There are %d offsets need to upload' % (len(offsets)))
            debug('Now start upload file blocks')
            if self.concurrency > 0:
                pool = ThreadPool(self.concurrency)
                pool.map(self._make_block, offsets)
                pool.close()
                pool.join()

            elif self.concurrency == 0:
                for offset in offsets:
                    return_code = self._make_block(offset)
                    if 400 <= int(return_code) <= 499:
                        debug('Single-Thread,attempt authentication failed,exit the task.')
                        sys.exit()
            else:
                raise ValueError('Invalid concurrency')
                sys.exit()

        if self._is_complete():
            debug('Now all blocks have upload suc.')
            mkfile_result = self._make_file()
            if 200 <= int(mkfile_result[0]) < 400:
                return mkfile_result
            else:
                raise WcsSeriveError("Make file fail,please upload file again")
        else:
            fail_list = self._get_failoffsets()
            upload_record = str(Config.tmp_record_folder) + self.uploadBatch
            debug('Sorry! Mulitpart upload fail,more detail see %s' % upload_record)
            # return self.results
            raise WcsSeriveError("Multipart upload fail,please upload file again")
