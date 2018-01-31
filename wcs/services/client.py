from wcs.commons.util import urlsafe_base64_encode
from wcs.commons.auth import Auth
from wcs.services.simpleupload import SimpleUpload
from wcs.services.streamupload import StreamUpload
from wcs.services.multipartupload import MultipartUpload
from wcs.services.filemanager import BucketManager
from wcs.services.fmgr import Fmgr
from wcs.services.persistentfop import PersistentFop
from wcs.services.wslive import WsLive
from wcs.commons.putpolicy import PutPolicy

class Client(object):
    
    def __init__(self, config):
        self.auth = Auth(config.access_key, config.secret_key)
        self.simpleupload = SimpleUpload(config.put_url)
        self.streamupload = StreamUpload(config.put_url)
        self.multiupload = MultipartUpload(config.put_url)
        self.bmgr = BucketManager(self.auth,config.mgr_url)
        self.fmgr = Fmgr(self.auth,config.mgr_url)
        self.pfops = PersistentFop(self.auth,config.mgr_url)
        self.wsl = WsLive(self.auth,config.mgr_url)
        self.cfg = config         

    def simple_upload(self, path, bucket, key):
        policy = PutPolicy()
        policy.set_conf('scope', '%s:%s' % (bucket,key))
        policy.dump_policy(self.cfg)
        token = self.auth.uploadtoken(policy.putpolicy)
        return self.simpleupload.upload(path,token)

    def stream_upload(self, stream, bucket, key):
        policy = PutPolicy()
        policy.set_conf('scope', '%s:%s' % (bucket,key))
        policy.dump_policy(self.cfg)
        token = self.auth.uploadtoken(policy.putpolicy)
        return self.streamupload.upload(stream,token)

    def multipart_upload(self,path,bucket, key,tmp_upload_id=None):
        policy = PutPolicy()
        policy.set_conf('scope', '%s:%s' % (bucket,key))
        policy.dump_policy(self.cfg)
        token = self.auth.uploadtoken(policy.putpolicy)
        upload_id = tmp_upload_id or self.cfg.upload_id
        return self.multiupload.upload(path,token,upload_id)
        
    def bucket_list(self,bucket,prefix=None, marker=None, limit=None, mode=None):
        try:
            pre = prefix or str(self.cfg.prefix)
        except Error:
            pre = ''
        
        try:
            m = mode or int(self.cfg.mode)
        except Error:
            m = ''
        
        try:
            mar = marker or str(self.cfg.marker)
        except Error:
            mar = ''
        try:
            l = limit or int(self.cfg.limit)
        except Error:
            l = ''
        return self.bmgr.bucketlist(bucket,pre,mar,l,m)

    def list_buckets(self):
        return self.bmgr.bucket_list()
   
    def bucket_stat(self, name, startdate, enddate):
        return self.bmgr.bucket_stat(name, startdate, enddate)

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

    def _parse_fops(self, fops):
        data = [fops]
        if self.cfg.notifyurl:
            data.append('notifyURL=%s' % urlsafe_base64_encode(self.cfg.notifyurl))
        if self.cfg.separate: 
            data.append('separate=%s' % self.cfg.separate)
        if self.cfg.force:
            data.append('force=%s' % self.cfg.force)
        return 'fops=' + '&'.join(data)

    def fmgr_move(self, fops):
        return self.fmgr.fmgr_move(self._parse_fops(fops))

    def fmgr_copy(self, fops): 
        return self.fmgr.fmgr_copy(self._parse_fops(fops))

    def fmgr_fetch(self, fops):
        return self.fmgr.fmgr_fetch(self._parse_fops(fops))

    def fmgr_delete(self, fops):
        return self.fmgr.fmgr_delete(self._parse_fops(fops))

    def prefix_delete(self, fops):
        return self.fmgr.prefix_delete(self._parse_fops(fops))

    def m3u8_delete(self, fops):
        return self.fmgr.m3u8_delete(self._parse_fops(fops))

    def fmgr_status(self,persistentId):
        return self.fmgr.status(persistentId)

    def ops_execute(self,fops,bucket,key):
        f = int(self.cfg.force)
        if self.cfg.separate:
            separate = int(self.cfg.separate)
        else:
            separate = 0
        notifyurl = self.cfg.notifyurl or ''
        return self.pfops.execute(fops,bucket,key,f,separate,notifyurl)
 
    def ops_status(self,persistentId):
        return self.pfops.fops_status(persistentId)

    def wslive_list(self,channelname, startTime, endTime, bucket, start=None, limit=None):
        return self.wsl.wslive_list( channelname, startTime, endTime, bucket, start, limit)

