from wcs.commons.util import urlsafe_base64_encode
from wcs.commons.config import Config
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
        
    def bucket_list(self,bucket,prefix=None,marker=None,limit=None,mode=None):
        return self.bmgr.bucketlist(bucket,prefix,marker,limit,mode)

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
        if Config.notifyurl:
            data.append('notifyURL=%s' % urlsafe_base64_encode(Config.notifyurl))
        if Config.separate: 
            data.append('separate=%s' % Config.separate)
        return 'fops=' + '&'.join(data)

    def _commons(self,srcbk,srckey,dstbk,dstkey=None,prefix=None):
        resource = urlsafe_base64_encode('%s:%s' % (srcbk,srckey))
        fops = 'resource/%s/bucket/%s' % (resource,urlsafe_base64_encode(dstbk))
        if dstkey:
            fops += '/key/%s'% urlsafe_base64_encode(dstkey)
        if prefix:
            fops += '/prefix/%s' % urlsafe_base64_encode(prefix)
        return fops
        
    def fmgr_move(self,srcbk,srckey,dstbk,dstkey,prefix=None):
        fops = self._commons(srcbk,srckey,dstbk,dstkey,prefix)
        return self.fmgr.fmgr_move(self._parse_fops(fops))

    def fmgr_copy(self,srcbk,srckey,dstbk,dstkey,prefix=None): 
        fops = self._commons(srcbk,srckey,dstbk,dstkey,prefix)
        return self.fmgr.fmgr_copy(self._parse_fops(fops))

    def fmgr_fetch(self,url,bucket,key,prefix=None,md5=None,decompre=None):
        fops = 'fetchURL/%s/bucket/%s' % (urlsafe_base64_encode(url),urlsafe_base64_encode(bucket))
        if prefix:
            fops +=  '/prefix/%s' % urlsafe_base64_encode(prefix)
        if md5:
            fops +=  '/md5/%s' % md5
        if decompre:
            fops += '/decompressioin/%s' % decompre
        return self.fmgr.fmgr_fetch(self._parse_fops(fops))

    def fmgr_delete(self,bucket,key):
        fops = 'bucket/%s/key/%s' % (urlsafe_base64_encode(bucket),urlsafe_base64_encode(key))
        return self.fmgr.fmgr_delete(self._parse_fops(fops))

    def prefix_delete(self,bucket, prefix):
        fops = 'bucket/%s/prefix/%s' % (urlsafe_base64_encode(bucket), urlsafe_base64_encode(prefix))
        if Config.output:
            fops += '/output/%s' % urlsafe_base64_encode(Config.output)
        data = [fops]
        if Config.notifyurl:
            data.append('notifyURL=%s' % urlsafe_base64_encode(Config.notifyurl))
        if Config.separate: 
            data.append('separate=%s' % Config.separate)
        reqdata = 'fops=' + '&'.join(data)  
        return self.fmgr.prefix_delete(reqdata)

    def m3u8_delete(self,bucket,key,delete=1):
        fops = 'bucket/%s/key/%s/deletes/%d' % (bucket,key,delete)
        return self.fmgr.m3u8_delete(self._parse_fops(fops))

    def fmgr_status(self,persistentId):
        return self.fmgr.status(persistentId)

    def ops_execute(self,fops,bucket,key):
        f = int(Config.force)
        separate = int(Config.separate) 
        notify = Config.notifyurl or ''
        return self.pfops.execute(fops,bucket,key,force,separate,notifyurl)
 
    def ops_status(self,persistentId):
        return self.pfops.fops_status(persistentId)

    def wslive_list(self,channelname, startTime, endTime, bucket, start=None, limit=None):
        return self.wsl.wslive_list( channelname, startTime, endTime, bucket, start, limit)

