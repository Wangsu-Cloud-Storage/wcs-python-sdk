import json
import os
import string
import subprocess
import requests
import tempfile
import time
import unittest

from wcs.commons.auth import Auth
from wcs.services.regupload import RegUpload
from wcs.services.sliceupload import SliceUpload
from wcs.services.filemanager import BucketManager
from wcs.services.fmgr import Fmgr
from wcs.services.persistentfop import PersistentFop
from wcs.services.streamupload import StreamUpload
from wcs.services.uploadprogressrecorder import UploadProgressRecorder
from wcs.services.wslive import WsLive

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        dummy_access_key = '1234'
        dummy_secret_key = 'qwer'
        self.dummy_auth = Auth(dummy_access_key,dummy_secret_key)

    def test_upload_token(self):
        putpolicy = {"scope":"test"}
        token = self.dummy_auth.uploadtoken(putpolicy)
        assert token == '1234:OWE0NTdhNDk4MzJiZGIwODlkMWFiYmFmMGRjNjIzMThlOWEyZGUxMg==:eyJzY29wZSI6ICJ0ZXN0In0='
   
    def test_manager_token(self):
        token = self.dummy_auth.managertoken('http://apitest.mgr0.v1.wcsapi.com/list?bucket=test')
        assert token == '1234:ZjE3NTA4Mjg1NGMyOTg4ZjNlODRlOWI3M2JhYTA3ZWVjZTM4NzM3ZA=='

class RegUploadTestCase(unittest.TestCase):
    def setUp(self):
        access_key = 'db17ab5d18c137f786b67c490187317a0738f94a'
        secret_key = 'b19958e080eb3b219628f50c20c9024f4ff1b140'
        self.auth = Auth(access_key, secret_key)
        #self.callback = 'http://callback-test.wcs.biz.matocloud.com:8088/callbackUrl'
        self.callback = 'http://61.130.27.208:8080/callbackurl'
        #self.notify = 'http://callback-test.wcs.biz.matocloud.com:8088/notifyUrl'
        self.notify = 'http://61.130.27.208:8080/notifyurl'
        self.detect = 'http://callback-test.wcs.biz.matocloud.com:8088/detectNotifyUrl'
        self.smallfile = '/root/rpm.log'

    def test_regupload(self):
        putpolicy = {'scope':'lumj-test:regupload-4-12.php', 'deadline':'1496130936000','overwrite':1}
        uploadtoken = self.auth.uploadtoken(putpolicy)
        regupload = RegUpload(uploadtoken)
        status_code, text = regupload.reg_upload(self.smallfile)
        assert status_code == 200
    
    def test_callback(self):
        putpolicy = {'scope':'lumj-test:callback.php', 'deadline':'1493607158000','callbackUrl':self.callback,'callbackBody':'bucket=$(bucket)&key=$(key)','overwrite':1}
        uploadtoken = self.auth.uploadtoken(putpolicy)
        regupload = RegUpload(uploadtoken)
        status_code,text = regupload.reg_upload(self.smallfile)
        assert status_code == 200 or status_code == 579

    def test_notify(self):
        ops = 'watermark/png/mode/1/dissolve/50|saveas/bHVtai10ZXN0OnF3YXItZm9wcw=='
        putpolicy = {'scope':'lumj-test:qware-2-23.jpg','deadline':'1493607158000','persistentNotifyUrl':self.notify,'persistentOps':ops,'overwrite':1,'returnBody':'key=$(key)&persistentId=$(persistentId)&fsize=$(fsize)'}
        uploadtoken = self.auth.uploadtoken(putpolicy)
        regupload = RegUpload(uploadtoken)
        status_code,text = regupload.reg_upload(self.smallfile)
        assert status_code == 200

    def test_detect(self):
        putpolicy = {'scope':'lumj-test:detect.log', 'deadline':'1490803200000','overwrite':1}
        putpolicy['contentDetect'] = 'imagePorn'
        putpolicy['detectNotifyURL'] = self.detect
        putpolicy['detectNotifyRule'] = 'all'
        uploadtoken = self.auth.uploadtoken(putpolicy)
        regupload = RegUpload(uploadtoken)
        status_code, text = regupload.reg_upload(self.smallfile)
        assert status_code == 200

class StreamUploadTestCase(unittest.TestCase):

    def setUp(self):
        putpolicy = {'scope':'lumj-test:stream.ts', 'deadline':'1493607158000','overwrite':1}
        access_key = 'db17ab5d18c137f786b67c490187317a0738f94a'
        secret_key = 'b19958e080eb3b219628f50c20c9024f4ff1b140'
        auth = Auth(access_key, secret_key)
        self.uploadtoken = auth.uploadtoken(putpolicy)

    def test_upload(self):
        #stream = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1491991315689&di=6918dba55bdbfd039f79eb9891f9e392&imgtype=0&src=http%3A%2F%2Fphoto.iyaxin.com%2Fattachement%2Fjpg%2Fsite2%2F20120402%2F001966720af110e381132c.jpg'
        stream = 'http://plu-test001.d.wcsapi.biz.matocloud.com/9da9b1a67d1e47d4a5dafcb9a16ad958_0000003.ts'
        streamupload = StreamUpload(self.uploadtoken)
        status_code, text = streamupload.upload(stream)
        assert status_code == 200

class SliceUploadTestCase(unittest.TestCase):

    def setUp(self):
        putpolicy = {'scope':'lumj-test:python.tar', 'deadline':'1496130936000','overwrite':1}
        access_key = 'db17ab5d18c137f786b67c490187317a0738f94a'
        secret_key = 'b19958e080eb3b219628f50c20c9024f4ff1b140'
        auth = Auth(access_key, secret_key)
        uploadtoken = auth.uploadtoken(putpolicy)
        bucket = 'lumj-test'
        key = 'python.tar'
        param = {'position':'local','message':'upload'}
        modify_time = time.time()
        upload_progress_recorder = UploadProgressRecorder()
        self.bigfile = '/root/Python-3.5.1.tar'
        self.sliceupload = SliceUpload(uploadtoken, self.bigfile, key, param, upload_progress_recorder, modify_time)
    
    def test_upload(self):
        code, hashvalue = self.sliceupload.slice_upload()
        print (code, hashvalue)
        assert code == 200

class BucketManagerTestCase(unittest.TestCase):

    def setUp(self):
        access_key = 'db17ab5d18c137f786b67c490187317a0738f94a'
        secret_key = 'b19958e080eb3b219628f50c20c9024f4ff1b140'
        #access_key = '18e25eb325c4e61ea361dff6990263f95a304c02'
        #secret_key = 'ba50ecb46f63755df1b5186c6b9bfd0b76de62c9'
        auth = Auth(access_key, secret_key)
        self.filemanager = BucketManager(auth)
        self.bucket = 'lumj-test'
        self.key = 'regupload-12-23-2.jpg'
        self.deadline = 1
        self.delkey = 'copy'
        self.srckey = 'test_notify'
        self.copykey = 'copy'
        self.movekey = 'move'
        self.image = 'callback-12-23-2.jpg'
        self.vedio = 'dontforgetme.mp4'

    def test_list(self):
        code,text = self.filemanager.bucketlist(self.bucket,limit=2000,prefix='c2xpY2U=')
        assert code == 200

    def test_stat(self):
        code,text = self.filemanager.stat(self.bucket,self.key)
        assert code == 200

    def test_delete(self):
        code,text = self.filemanager.delete(self.bucket,self.movekey) 
        assert code == 200

    def test_move(self):
        code, text = self.filemanager.move(self.bucket, self.copykey, self.bucket, self.movekey)
        assert code == 200

    def test_copy(self):
        code, text = self.filemanager.copy(self.bucket, self.key, self.bucket, self.copykey)
        assert code == 200

    def test_setDL(self):
        code, text = self.filemanager.setdeadline(self.bucket, self.key, self.deadline) 
        assert code == 200


class FmgrTestCase(unittest.TestCase):
    def setUp(self):
        access_key = 'db17ab5d18c137f786b67c490187317a0738f94a'
        secret_key = 'b19958e080eb3b219628f50c20c9024f4ff1b140'
        auth = Auth(access_key, secret_key)
        self.filemanager = Fmgr(auth)
        self.bucket = 'lumj-test'
        self.copyfops = 'resource/bHVtai10ZXN0OmZpcnN0LmpwZw==/bucket/bHVtai10ZXN0/key/Y29weS10ZXN0LmpwZw=='
        self.fops = 'resource/bHVtai10ZXN0OjEuZG9j/bucket/bHVtai10ZXN0/key/Zm9wcy5kb2M='
        self.movefops = 'resource/bHVtai10ZXN0OkNocnlzYW50aGVtdW0uanBn/bucket/bHVtai10ZXN0/key/dGVzdF9tb3ZlLmpwZw==/prefix/dGVzdG1vdmU='
        self.notify = 'http://callback-test.wcs.biz.matocloud.com:8088/notifyUrl'
        self.key = 'Chrysanthemum.jpg' 
        self.fetfops = 'fetchURL/aHR0cDovL2x1bWotdGVzdC5zLndjc2FwaS5iaXoubWF0b2Nsb3VkLmNvbS9xd2FyLWZvcHM=/bucket/bHVtai10ZXN0/key/ZmV0Y2h0ZXN0ZmlsZQ=='
        self.delfops = 'bucket/bHVtai10ZXN0/key/ZmV0Y2h0ZXN0ZmlsZQ=='
        self.prefops = 'bucket/bHVtai10ZXN0/prefix/dGVzdG1vdmU='
        self.m3u8fops = 'bucket/d3V5aWt1bg==/key/MTAzX29yaWdpbmFsLm0zdTg=/deletets/1'
 
    def test_copy(self):
        code,text = self.filemanager.fmgr_copy(self.copyfops,notifyurl=self.notify,separate=1)
        assert code == 200

    def test_move(self):
        code,text = self.filemanager.fmgr_move(self.movefops,notifyurl=self.notify,separate=1)
        assert code == 200

    def test_fetch(self):
        code,text = self.filemanager.fmgr_fetch(self.fetfops,notifyurl=self.notify,separate=1)
        assert code == 200

    def test_delete(self):
        code,text = self.filemanager.fmgr_delete(self.delfops,notifyurl=self.notify,separate=1)
        assert code == 200

    def test_pre_delete(self):
        code, text = self.filemanager.prefix_delete(self.prefops, notifyurl=self.notify, separate=1)
        assert code == 200

    def test_m3u8_delete(self):
        code, text = self.filemanager.m3u8_delete(self.m3u8fops, notifyurl=self.notify, separate=1)
        assert code == 200
            
    def test_status(self):
        persistentId = '100086aac2ff755b4a32b6f88841777070cd'
        code,text = self.filemanager.status(persistentId)
        assert code == 200

class PerFopTestCase(unittest.TestCase):

    def setUp(self):
        access_key = 'db17ab5d18c137f786b67c490187317a0738f94a'
        secret_key = 'b19958e080eb3b219628f50c20c9024f4ff1b140'
        auth = Auth(access_key, secret_key)
        self.fops = PersistentFop(auth,'lumj-test')
        self.ops = 'vframe/jpg/offset/10/w/1000/h/1000|saveas/bHVtai10ZXN0OnZmcmFtZS10ZXN0LTEwLmpwZw=='
        self.statusops = 'vframe/jpg/offset/10/w/1000/h/1000|saveas/bHVtai10ZXN0OnZmcmFtZS1zdGF0dXMtNC5qcGc='
        self.notify = 'http://callback-test.wcs.biz.matocloud.com:8088/notifyUrl'
        self.key = 'video_sync.mp4'
        self.persistentId = ''

    def test_fops(self):
        code,text = self.fops.execute(self.ops,self.key,force=1,notifyurl=self.notify)
        assert code == 200

    def test_status(self):
        persistentId = '1000dcaa6bb559eb40b698549f3843b6afb0'
        code,text = self.fops.fops_status(persistentId)
        assert code == 200

class WsLiveTestCase(unittest.TestCase):

    def setUp(self):
        #access_key = '1b007666ab862a94599e8e50b62f7a8dfbab2dbd'
        #secret_key = '6d98979e12f3872c3e1ccb1fb103df80699f2a1d'
        access_key = '386f2a22a60a032298dfc86565bf0631de550b4f'
        secret_key = '05f7d0d024da3b4870beb2e88160e583751258a0'
        auth = Auth(access_key, secret_key)
        self.wslive = WsLive(auth)
        self.channelname = 'hudong-stream-6390098616488299266'
        self.startTime = '20161227095704'
        self.endTime = '20161227101643'
        self.bucket = 'live-hls'

    def test_wslivelist(self):
        code, text = self.wslive.wslive_list(self.channelname, self.startTime, self.startTime, self.bucket)
        assert code == 200


if __name__ == '__main__':
    unittest.main()

