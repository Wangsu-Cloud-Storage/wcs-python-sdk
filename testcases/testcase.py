import os,sys
import unittest
from os.path import expanduser
sys.path.append('../')
from wcs.commons.config import Config
from wcs.services.client import Client
from wcs.commons.putpolicy import PutPolicy
from wcs.commons.logme import debug
from wcs.commons.util import urlsafe_base64_encode,etag

config_file = os.path.join(expanduser("~"), ".wcscfg")

class WcsTestCases(unittest.TestCase):
    
    def setUp(self):
        self.cfg = Config(config_file)
        self.cli = Client(self.cfg)
        self.bucket = 'qz-region98-restupload-caiyz'
 
    # 普通上传
    def test_simple_upload(self):
        key = '20180408.jpg'
        path = 'E:\\simpleupload.py'
        return_data = self.cli.simple_upload(path, self.bucket, key)
        debug(return_data)
        debug(return_data[0])

    # 流数据上传
    def test_stream_upload(self):
        stream = 'http://www.example.com/1.doc'
        key = '1.doc'
        debug(self.cli.stream_upload(stream, self.bucket, key))
    
    # 分片上传
    def test_multipart_upload(self):
        path = ''
        key = ''
        debug(self.cli.multipart_upload(path, self.bucket, key))
        
    # 智能上传（文件大于10M启用分片上传，有同名文件直接覆盖）
    def test_samrt_upload(self):
        path = '/root/caiyz/data/14M'
        key = '100-2M'
        self.cfg.overwrite =1
        debug(self.cli.smart_upload(path, self.bucket, key, multi_size=10))
        
    def test_bucket_list(self):
        debug(self.cli.bucket_list(self.bucket))

    def test_bucket_stat(self):
        startdate = '2019-01-10'
        enddate = '2019-01-12'
        debug(self.cli.bucket_stat(self.bucket, startdate, enddate))

    def test_stat(self):
        key = ''
        debug(self.cli.stat(self.bucket, key))

    def test_delete(self):
        key = ''
        debug(self.cli.delete(self.bucket,key))

    def test_move(self):
        srckey = ''
        dstkey = ''
        debug(self.cli.move(self.bucket, srckey, self.bucket,dstkey))

    def test_copy(self):
        srckey = ''
        dstkey = ''
        debug(self.cli.copy(self.bucket, srckey, self.bucket,dstkey))
    
    def test_setdeadline(self):
        key = ''
        deadline = ''
        debug(self.cli.setdeadline(self.bucket, key, deadline))

    def test_fmgr_move(self):
        srckey = ''
        dstkey = ''
        resource = urlsafe_base64_encode('%s:%s' % (self.bucket,srckey))
        fops = 'resource/%s/bucket/%s/key/%s' % (resource,urlsafe_base64_encode(self.bucket), urlsafe_base64_encode(dstkey))
        debug(self.cli.fmgr_move(fops))
        
    def test_fmgr_copy(self):
        srckey = ''
        dstkey = ''
        resource = urlsafe_base64_encode('%s:%s' % (self.bucket,srckey))
        fops = 'resource/%s/bucket/%s/key/%s' % (resource,urlsafe_base64_encode(self.bucket), urlsafe_base64_encode(dstkey))
        debug(self.cli.fmgr_copy(fops))

    def test_fmgr_fetch(self):
        url = 'http://www.example.com/1.doc'
        key = ''
        fetchurl = urlsafe_base64_encode(url)
        enbucket = urlsafe_base64_encode(self.bucket)
        enkey = urlsafe_base64_encode(key)
        fops = 'fetchURL/%s/bucket/%s/key/%s' % (fetchurl, enbucket, enkey)
        debug(self.cli.fmgr_fetch(fops))

    def test_fmgr_delete(self):
        key = ''
        enbucket = urlsafe_base64_encode(self.bucket)
        enkey = urlsafe_base64_encode(key)
        fops = 'bucket/%s/key/%s' % (enbucket, enkey)
        debug(self.cli.fmgr_delete(fops))

    def test_fmgr_prefix_del(self):
        prefix = ''
        enbucket = urlsafe_base64_encode(self.bucket)
        enprefix = urlsafe_base64_encode(prefix)
        fops = 'bucket/%s/prefix/%s' % (enbucket, enprefix)
        debug(self.cli.prefix_delete(fops))

    def test_fmgr_m3u8_del(self):
        key = ''
        enbucket = urlsafe_base64_encode(self.bucket) 
        enkey = urlsafe_base64_encode(key)
        fops = 'bucket/%s/key/%s' % (enbucket, enkey)
        debug(self.cli.m3u8_delete(fops))

    def test_fmgr_stat(self):
        persistentId = ''
        debug(self.cli.fmgr_status(persistentId))

    def test_ops(self):
        key = ''
        fops = ''
        debug(self.cli.ops_execute(fops,self.bucket,key))

    def test_ops_status(self):
        persistentId = ''
        debug(self.cli.ops_status(persistentId)) 

    #查询统计数据
    def test_bucket_statistics(self):
        return_data = self.cli.bucket_statistics(self.bucket, 'uploadRequest', '2019-12-20', '2019-12-31')
        debug(return_data)
        self.assertEqual(return_data[0],200)

    def test_imageDetect(self):
        bucket = 'qz-caiyz-rgwonly'
        dtype = 'porn'
        imageurl = 'https://www.google.com.hk/52380062482021'
        debug(self.cli.image_detect(bucket,dtype,imageurl))

    def test_wslive_list(self):
        channel = ''
        startTime = ''
        endTime = ''
        debug(self.cli.wslive_list(channel, startTime, endTime,self.bucket))

    def test_etag(self):
        print(etag('D:\\itools\\spacesniffer1302.zip'))

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(WcsTestCases("test_simple_upload"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
