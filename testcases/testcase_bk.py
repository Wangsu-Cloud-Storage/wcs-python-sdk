import os,sys
import unittest
from os.path import expanduser
from wcs.commons.config import Config
from wcs.services.client import Client
from wcs.commons.putpolicy import PutPolicy
from wcs.commons.logme import debug
from wcs.commons.util import urlsafe_base64_encode

config_file = os.path.join(expanduser("~"), ".wcscfg")

class WcsTestCases(unittest.TestCase):
    
    def setUp(self):
        self.cfg = Config(config_file)
        self.cli = Client(self.cfg)
        self.bucket = 'ezvizws-test'
 
    def test_simple_upload(self):
        key = 'small'
        path = '/root/MegaSAS.log'
        debug(self.cli.simple_upload(path, self.bucket, key))

    def test_stream_upload(self):
        stream = 'http://www.example.com/1.doc'
        key = '1.doc'
        debug(self.cli.stream_upload(stream, self.bucket, key))
        
    def test_multipart_upload(self):
        big = '/root/liuxj/test-100M'
        key = 'test-100M-2018'
        debug(self.cli.multipart_upload(big, self.bucket, key))
        
    def test_bucket_list(self):
        debug(self.cli.bucket_list(self.bucket))

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
        resource = urlsafe_base64_encode('%s:%s' % (self.bucket,srckey))
        fops = 'resource/%s/bucket/%s/key/%s' % (resource,urlsafe_base64_encode(self.bucket), urlsafe_base64_encode(dstkey))
        debug(self.cli.fmgr_move(fops))
        
    def test_fmgr_copy(self):
        srckey = '2.doc'
        dstkey = '1.doc'
        resource = urlsafe_base64_encode('%s:%s' % (self.bucket,srckey))
        fops = 'resource/%s/bucket/%s/key/%s' % (resource,urlsafe_base64_encode(self.bucket), urlsafe_base64_encode(dstkey))
        debug(self.cli.fmgr_copy(fops))

    def test_fmgr_fetch(self):
        url = 'http://a20170704-weihb.w.wcsapi.biz.matocloud.com/1.doc'
        key = '1.doc'
        fetchurl = urlsafe_base64_encode(url)
        enbucket = urlsafe_base64_encode(self.bucket)
        enkey = urlsafe_base64_encode(key)
        fops = 'fetchURL/%s/bucket/%s/key/%s' % (fetchurl, enbucket, enkey)
        debug(self.cli.fmgr_fetch(fops))

    def test_fmgr_delete(self):
        key = '1.doc'
        enbucket = urlsafe_base64_encode(self.bucket)
        enkey = urlsafe_base64_encode(key)
        fops = 'bucket/%s/key/%s' % (enbucket, enkey)
        debug(self.cli.fmgr_delete(fops))

    def test_fmgr_prefix_del(self):
        prefix = 'test'
        enbucket = urlsafe_base64_encode(self.bucket)
        enprefix = urlsafe_base64_encode(prefix)
        fops = 'bucket/%s/prefix/%s' % (enbucket, enprefix)
        debug(self.cli.prefix_delete(fops))

    def test_fmgr_m3u8_del(self):
        key = 'Wildlife111.wmv'
        enbucket = urlsafe_base64_encode(self.bucket) 
        enkey = urlsafe_base64_encode(key)
        fops = 'bucket/%s/key/%s' % (enbucket, enkey)
        debug(self.cli.m3u8_delete(fops))

    def test_fmgr_stat(self):
        persistentId = '2012dee7ddcbfbde413f98e58d8981348bf8'
        persistentId = '1000dd9a6a1991b34924a4dde3eaec15c42f'
        debug(self.cli.fmgr_status(persistentId))

    def test_ops(self):
        key = 'Wildlife111.wmv'
        fops = 'vframe/jpg/offset/1'
        debug(self.cli.ops_execute(fops,self.bucket,key))

    def test_ops_status(self):
        persistentId = ''
        debug(self.cli.ops_status(persistentId)) 

    def test_wslive_list(self):
        channel = ''
        startTime = ''
        endTime = ''
        debug(self.cli.wslive_list(channel, startTime, endTime,self.bucket)) 

if __name__ == '__main__':
    unittest.main()
