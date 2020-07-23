#!/usr/bin/python
## -*- coding: utf-8 -*-

from wcs.commons.http import _get
from wcs.commons.http import _post
from wcs.commons.logme import debug
from wcs.commons.util import https_check
from wcs.services.mgrbase import MgrBase


class Fmgr(MgrBase):
    """高级资源管理类
    高级资源管理继承自mgrbase
    """

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
    
    # 多文件压缩(https://wcs.chinanetcenter.com/document/API/Fmgr/compress)
    # add by laihy 20200224
    def fmgr_compress(self, reqdata):
        return self._fmgr_commons(reqdata, 'compress')
