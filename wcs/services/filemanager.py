from wcs.services.mgrbase import MgrBase
from wcs.commons.http import _post
from wcs.commons.http import _get
from wcs.commons.util import urlsafe_base64_encode, https_check, entry
from wcs.commons.config import Config
from wcs.commons.logme import debug, error
class BucketManager(MgrBase):

    def __init__(self, auth,mgr_url):
        super(BucketManager, self).__init__(auth,mgr_url)

    def _limit_check(self):
        n = 0
        while n < 1001:
            yield n
            n += 1

    def _make_delete_url(self, bucket, key):
        return '{0}/delete/{1}'.format(self.mgr_host, entry(bucket, key))

    def delete(self, bucket, key):
        url = https_check(self._make_delete_url(bucket, key))
        debug('Start to post request of delete %s:%s' % (bucket, key))
        return _post(url=url, headers=super(BucketManager, self)._gernerate_headers(url))

    def _make_filestat_url(self, bucket, key):
        return '{0}/stat/{1}'.format(self.mgr_host, entry(bucket, key))

    def stat(self, bucket, key):
        url = https_check(self._make_filestat_url(bucket, key))
        debug('Start to get the stat of %s:%s' % ( bucket, key))
        return _get(url=url, headers=super(BucketManager, self)._gernerate_headers(url))
 
    def _make_url(self, operation, param):
        url = ['{0}/{1}'.format(self.mgr_host,operation)]
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
            options['prefix'] = urlsafe_base64_encode(prefix)
        if mode:
            options['mode'] = mode
        url = https_check(self._make_url('list', options))
        if options:
            debug('List options is %s' % options)
        debug('List bucket %s' % bucket)
        return _get(url=url, headers=super(BucketManager, self)._gernerate_headers(url))

    def _make_move_url(self, srcbucket, srckey, dstbucket, dstkey):
        src = urlsafe_base64_encode('%s:%s' % (srcbucket, srckey))
        dst = urlsafe_base64_encode('%s:%s' % (dstbucket, dstkey)) 
        url = '{0}/move/{1}/{2}'.format(self.mgr_host, src, dst)
        return https_check(url)

    def move(self, srcbucket, srckey, dstbucket, dstkey):
        url = self._make_move_url(srcbucket, srckey, dstbucket, dstkey)
        debug('Move object %s from %s to %s:%s' % (srckey, srcbucket, dstbucket, dstkey))
        return _post(url=url, headers=super(BucketManager, self)._gernerate_headers(url))
 
    def _make_copy_url(self, srcbucket, srckey, dstbucket, dstkey):
        src = urlsafe_base64_encode('%s:%s' % (srcbucket, srckey))
        dst = urlsafe_base64_encode('%s:%s' % (dstbucket, dstkey))
        url = '{0}/copy/{1}/{2}'.format(self.mgr_host, src, dst)
        return https_check(url)

    def copy(self, srcbucket, srckey, dstbucket, dstkey):
        url = self._make_copy_url(srcbucket, srckey, dstbucket, dstkey)
        debug('Copy object %s from %s to %s:%s' % (srckey, srcbucket, dstbucket, dstkey))
        return _post(url=url, headers=super(BucketManager, self)._gernerate_headers(url))

    def setdeadline(self, bucket, key, deadline):
        url = https_check('{0}/setdeadline'.format(self.mgr_host))
        param = {
            'bucket' : urlsafe_base64_encode(bucket),
        }
        param['key'] = urlsafe_base64_encode(key) 
        param['deadline'] = deadline 
        body = super(BucketManager, self)._params_parse(param)
        debug('Set deadline of %s to %s' % (key, deadline))
        return _post(url=url, data=body, headers=super(BucketManager, self)._gernerate_headers(url, body))

    def bucket_list(self):
        url = '{0}/bucket/list'.format(self.mgr_host)
        url = https_check(url)
        debug('Now start to list buckets')
        return _get(url=url, headers=super(BucketManager, self)._gernerate_headers(url))

    def bucket_stat(self, name, startdate, enddate):
        encode_name = urlsafe_base64_encode(name)
        options = {'name':encode_name, 'startdate':startdate, 'enddate':enddate}
        url = https_check(self._make_url('bucket/stat', options))
        debug('Now check storage of %s from %s to %s' % (name, startdate, enddate))
        return _get(url=url, headers=super(BucketManager, self)._gernerate_headers(url))

        
