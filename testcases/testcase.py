import os
import unittest
from os.path import expanduser
from wcs.commons.config import Config
from wcs.services.client import Client
from wcs.commons.putpolicy import PutPolicy
from wcs.commons.logme import debug

config_file = os.path.join(expanduser("~"), ".wcscfg")

class WcsTestCases(unittest.TestCase):
    
    def setUp(self):
        self.cfg = Config(config_file)
        self.cli = Client(self.cfg)
        self.bucket = 'ezvizws-test'
 
    def test_simple_upload(self):
        key = 'MegaSAS.log'
        small = '/root/MegaSAS.log'
        debug(self.cli.simple_upload(small, self.bucket, key))

    def test_stream_upload(self):
        stream = 'http://a20170704-weihb.w.wcsapi.biz.matocloud.com/1.doc'
        key = '1.doc'
        debug(self.cli.stream_upload(stream, self.bucket, key))
        
    def test_multipart_upload(self):
        big = '/root/liuxj/test-100M'
        key = 'test-100M'
        debug(self.cli.multipart_upload(big, self.bucket, key, self.cfg.upload_id))
        
    def test_bucket_list(self):
        debug(self.cli.bucket_list(self.bucket,str(self.cfg.prefix), str(self.cfg.marker), int(self.cfg.limit),int(self.cfg.mode)))

    def test_bucket_stat(self):
        startdate = '2017-11-10'
        enddate = '2017-11-12'
        debug(self.cli.bucket_stat(self.bucket, startdate, enddate))

    def test_stat(self):
        key = 'MegaSAS.log'
        debug(self.cli.stat(self.bucket, key))

    def test_delete(self):
        key = 'test-100M'
        debug(self.cli.delete(self.bucket,key))

    def test_move(self):
        srckey = '1.doc'
        dstkey = '2.doc'
        debug(self.cli.move(self.bucket, srckey, self.bucket,dstkey))

    def test_copy(self):
        srckey = '2.doc'
        dstkey = '1.doc'
        debug(self.cli.copy(self.bucket, srckey, self.bucket,dstkey))
    
    def test_setdeadline(self):
        key = '1.doc'
        deadline = '10'
        debug(self.cli.setdeadline(self.bucket, key, deadline))

    def test_fmgr_move(self):
        srckey = '1.doc'
        dstkey = '2.doc'
        debug(self.cli.fmgr_move(self.bucket, srckey, self.bucket,dstkey))
        
    def test_fmgr_copy(self):
        srckey = '2.doc'
        dstkey = '1.doc'
        debug(self.cli.fmgr_copy(self.bucket, srckey, self.bucket,dstkey))

    def test_fmgr_fetch(self):
        url = 'http://a20170704-weihb.w.wcsapi.biz.matocloud.com/1.doc'
        key = '1.doc'
        debug(self.cli.fmgr_fetch(url,self.bucket,key,prefix="test"))

    def test_fmgr_delete(self):
        key = '1.doc'
        debug(self.cli.fmgr_delete(self.bucket,key))

    def test_fmgr_prefix_del(self):
        prefix = 'test'
        debug(self.cli.prefix_delete(self.bucket,prefix))

    def test_fmgr_m3u8_del(self):
        key = 'Wildlife111.wmv'
        debug(self.cli.m3u8_delete(self.bucket,key))

    def test_fmgr_stat(self):
        persistentId = '2012dee7ddcbfbde413f98e58d8981348bf8'
        debug(self.cli.fmgr_status(persistentId))

    def test_ops(self):
        fops = ''
        key = ''
        debug(self.cli.ops_execute(fops, self.bucket, key))

    def test_ops_status(self):
        persistentId = ''
        debug(self.cli.ops_status(persistentId)) 

    def test_wslive_list(self):
        channel = ''
        startTime = ''
        endTime = ''
        debug(self.cli.wslive_list(channel, startTime, endTime)) 

if __name__ == '__main__':
    unittest.main()
