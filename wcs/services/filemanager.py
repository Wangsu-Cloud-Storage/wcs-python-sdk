from wcs.services.mgrbase import MgrBase
from wcs.commons.http import _post
from wcs.commons.http import _get
from wcs.commons.logme import debug, warning, error
from wcs.commons.util import urlsafe_base64_encode, urlsafe_base64_decode,entry

class BucketManager(MgrBase):

    def __init__(self, auth,mgr_url):
        super(BucketManager, self).__init__(auth,mgr_url)

    def _limit_check(self):
        n = 0
        while n < 1000:
            yield n
            n += 1

    def _make_delete_url(self, bucket, key):
        return '{0}/delete/{1}'.format(self.mgr_host, entry(bucket, key))

    def delete(self, bucket, key):
        url = self._make_delete_url(bucket, key)
        debug('Start to post request of delete %s:%s' % (bucket, key))
        code, text = _post(url=url, headers=super(BucketManager, self)._gernerate_headers(url))
        debug('The return code is %d and text of delete request is: %s' % (code, text))
        return code, text

    def _make_filestat_url(self, bucket, key):
        return '{0}/stat/{1}'.format(self.mgr_host, entry(bucket, key))

    def stat(self, bucket, key):
        url = self._make_filestat_url(bucket, key)
        debug('Start to get the stat of %s:%s' % ( bucket, key))
        code, text = _get(url=url, headers=super(BucketManager, self)._gernerate_headers(url))
        debug('The return code : %d and text : %s' % (code, text))
        return code, text
 
    def _make_list_url(self, param):
        url = ['{0}/list'.format(self.mgr_host)]
        if param:
            url.append(super(BucketManager, self)._params_parse(param))
        url = '?'.join(url)
        return url
    
    def bucketlist(self, bucket, prefix=None, marker=None, limit=None, mode=None):
        options = {
            'bucket': bucket,
        }
        if marker:
            options['marker'] = marker
        if limit:
            if limit in self._limit_check():
                options['limit'] = limit
            else:
                error('Invalid limit ! Please redefine limit')
                raise ValueError("Invalid limit")
        if prefix:
            options['prefix'] = prefix
        if mode:
            options['mode'] = mode
        url = self._make_list_url(options)
        if options:
            debug('List options is %s' % options)
        debug('List bucket %s' % bucket)
        code, text = _get(url=url, data=options, headers=super(BucketManager, self)._gernerate_headers(url))
        debug('The return code : %d and text : %s' % (code, text))
        return code, text

    def _make_move_url(self, srcbucket, srckey, dstbucket, dstkey):
        src = urlsafe_base64_encode('%s:%s' % (srcbucket, srckey))
        dst = urlsafe_base64_encode('%s:%s' % (dstbucket, dstkey)) 
        url = '{0}/move/{1}/{2}'.format(self.mgr_host, src, dst)
        return url

    def move(self, srcbucket, srckey, dstbucket, dstkey):
        url = self._make_move_url(srcbucket, srckey, dstbucket, dstkey)
        debug('Move object %s from %s to %s:%s' % (srckey, srcbucket, dstbucket, dstkey))
        code, text = _post(url=url, headers=super(BucketManager, self)._gernerate_headers(url))
        debug('The return code : %d and text : %s' % (code, text))
        return code, text
 
    def _make_copy_url(self, srcbucket, srckey, dstbucket, dstkey):
        src = urlsafe_base64_encode('%s:%s' % (srcbucket, srckey))
        dst = urlsafe_base64_encode('%s:%s' % (dstbucket, dstkey))
        url = '{0}/copy/{1}/{2}'.format(self.mgr_host, src, dst)
        return url

    def copy(self, srcbucket, srckey, dstbucket, dstkey):
        url = self._make_copy_url(srcbucket, srckey, dstbucket, dstkey)
        debug('Copy object %s from %s to %s:%s' % (srckey, srcbucket, dstbucket, dstkey))
        code, text = _post(url=url, headers=super(BucketManager, self)._gernerate_headers(url))
        debug('The return code : %d and text : %s' % (code, text))
        return code, text

    def setdeadline(self, bucket, key, deadline):
        url = '{0}/setdeadline'.format(self.mgr_host)
        param = {
            'bucket' : urlsafe_base64_encode(bucket),
        }
        param['key'] = urlsafe_base64_encode(key) 
        param['deadline'] = deadline 
        body = super(BucketManager, self)._params_parse(param)
        debug('Set deadline of %s to %s' % (key, deadline))
        code, text = _post(url=url, data=body, headers=super(BucketManager, self)._gernerate_headers(url, body))
        debug('The return code : %d and text : %s' % (code, text))
        return code, text

    def uncompress(self,fops,bucket,key,notifyurl=None,force=None,separate=None):
        url = '%s/fops' % self.mgr_host
        options = {'bucket':urlsafe_base64_encode(bucket),'key':urlsafe_base64_encode(key),'fops':urlsafe_base64_encode(fops)}
        if notifyurl:
            options['notifyurl'] =urlsafe_base64_encode(notifyurl)
        if force:
            options['force'] = force
        if separate:
            options['separate'] = separate
        body = super(BucketManager, self)._params_parse(options)
        debug('Uncompress of %s : %s' % (bucket, key))
        code, text = _post(url=url, data=body, headers=super(BucketManager, self)._gernerate_headers(url, body))
        debug('The return code : %d and text : %s' % (code, text))
        return code,text
        

