from wcs.commons.auth import Auth
from wcs.services.simpleupload import SimpleUpload
from wcs.services.streamupload import StreamUpload
from wcs.services.multipartupload import MultipartUpload
from wcs.services.filemanager import BucketManager
from wcs.services.fmgr import Fmgr
from wcs.services.persistentfop import PersistentFop
from wcs.services.wslive import WsLive

class Client(object):
    
    def __init__(self, ak, sk, put_url, mgr_url):
        self.auth = Auth(ak, sk)
        self.simpleupload = SimpleUpload(put_url)
        self.streamupload = StreamUpload(put_url)
        self.multiupload = MultipartUpload(put_url)
        self.bmgr = BucketManager(self.auth,mgr_url)
        self.fmgr = Fmgr(self.auth,mgr_url)
        self.pfops = PersistentFop(self.auth,mgr_url)
        self.wsl = WsLive(self.auth,mgr_url)

    def simple_upload(self, path, policy):

        token = self.auth.uploadtoken(policy.putpolicy)
        return self.simpleupload.upload(path,token)

    def stream_upload(self, stream, policy):
        token = self.auth.uploadtoken(policy.putpolicy)
        return self.streamupload.upload(stream,token)

    def multipart_upload(self,path,policy,params=None):
        token = self.auth.uploadtoken(policy.putpolicy)
        return self.multiupload.upload(path,token,params)
        
    def list(self,bucket,prefix=None,marker=None,limit=None,mode=None):
        return self.bmgr.bucketlist(bucket,prefix,marker,limit,mode)

    def stat(self,bucket,key):
        return self.bmgr.stat(bucket,key)

    def delete(self,bucket,key):
        return self.bmgr.delete(bucket,key)

    def move(self,srcbucket, srckey, dstbucket, dstkey):
        return self.bmgr.move(srcbucket, srckey, dstbucket, dstkey)

    def copy(self,srcbucket, srckey, dstbucket, dstkey):
        return self.bmgr.copy(srcbucket, srckey, dstbucket, dstkey)

    def setdeadline(self,bucket,key,deadline):
        return self.bmgr.setdeadline(bucket,key,deadline)

    def uncompress(self,fops,bucket,key,notifyurl=None,force=None,separate=None):
         return self.bmgr.uncompress(fops,bucket,key,notifyurl,force,separate)

    def fmgr_move(self,fops,notifyurl=None,separate=None):
        return self.fmgr.fmgr_move(fops,notifyurl,separate)

    def fmgr_copy(self,fops,notifyurl=None,separate=None): 
        return self.fmgr.fmgr_copy(fops,notifyurl,separate)

    def fmgr_fetch(self,fops,notifyurl=None,separate=None):
        return self.fmgr.fmgr_fetch(fops,notifyurl,separate)

    def fmgr_delete(self,fops,notifyurl=None,separate=None):
        return self.fmgr.fmgr_delete(fops,notifyurl,separate)

    def prefix_delete(self,fops,notifyurl=None,separate=None): 
        return self.fmgr.prefix_delete(fops,notifyurl,separate)

    def m3u8_delete(self,fops,notifyurl=None,separate=None):
        return self.fmgr.m3u8_delete(fops,notifyurl,separate)

    def fmgr_status(self,persistentId):
        return self.fmgr.status(persistentId)

    def ops_execute(self,fops,bucket,key,force=None,separate=None,notifyurl=None):
        return self.pfops.execute(fops,bucket,key,force,separate,notifyurl)
 
    def ops_status(self,persistentId):
        return self.pfops.fops_status(persistentId)

    def wslive_list(self,channelname, startTime, endTime, bucket, start=None, limit=None):
        return self.wsl.wslive_list( channelname, startTime, endTime, bucket, start, limit)

