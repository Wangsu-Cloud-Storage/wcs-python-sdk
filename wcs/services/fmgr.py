from wcs.services.mgrbase import MgrBase
from wcs.commons.http import _post
from wcs.commons.http import _get
from wcs.commons.util import urlsafe_base64_encode,https_check

from wcs.commons.logme import debug, error

class Fmgr(MgrBase):

    def __init__(self, auth,url):
        super(Fmgr, self).__init__(auth,url)

    def _fmgr_commons(self, reqdata, method):
        url = https_check('{0}/fmgr/{1}'.format(self.mgr_host,method))
        debug('Request body is: %s' % (reqdata))
        debug('Start to execute opration: %s' % method)
        return _post(url=url, data=reqdata, headers=super(Fmgr, self)._gernerate_headers(url, body=reqdata)) 
        
    def fmgr_move(self, reqdata):
        return self._fmgr_commons(reqdata, 'move')

    def fmgr_copy(self, reqdata):
        return self._fmgr_commons(reqdata, 'copy')
   
    def fmgr_fetch(self, reqdata):
        return self._fmgr_commons(reqdata, 'fetch') 

    def fmgr_delete(self, reqdata):
        return self._fmgr_commons(reqdata,'delete')

    def prefix_delete(self, reqdata):
        return self._fmgr_commons(reqdata,'deletePrefix')

    def m3u8_delete(self, reqdata):
        return self._fmgr_commons(reqdata, 'deletem3u8')
   
    def status(self, persistentId):
        url = '{0}/fmgr/status?persistentId={1}'.format(self.mgr_host, persistentId)
        url = https_check(url)
        debug('Start to get status of persistentId: %s' % persistentId)
        return _get(url=url)
