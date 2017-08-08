import base64
import json
from wcs.commons.auth import Auth
from wcs.commons.config import MGR_URL
from wcs.commons.config import logging_folder
from wcs.commons.http import _post
from wcs.commons.http import _get
from wcs.commons.util import entry
from wcs.commons.util import urlsafe_base64_encode
from wcs.commons.logme import debug, warning, error

class Fmgr(object):

    def __init__(self, auth):
        self.auth = auth
        self.host = MGR_URL

    def gernerate_headers(self,url,body=None):
        token = self.auth.managertoken(url,body=body)
        headers = {'Authorization': token}
        return headers
        
    def params_parse(self, params):
        if params:
            paramlist = [] 
            for k, v in params.items():
                paramlist.append('{0}={1}'.format(k, v))
            paramlist = '&'.join(paramlist) 
        return paramlist

    def fmgr_move(self, fops,notifyurl=None,separate=None):
        url = '{0}/fmgr/move'.format(self.host)
        data = {'fops': fops}
        if notifyurl is not None:
            data['notifyURL'] = urlsafe_base64_encode(notifyurl)
        if separate is not None:
            data['separate'] = separate
        reqdata = self.params_parse(data)
        debug('Fmgr_move request body is: %s' % reqdata)
        debug('Start to move file')
        code, text = _post(url=url, data=reqdata, headers=self.gernerate_headers(url, body=reqdata))
        debug('The return code : %d ,text : %s' % (code, text))
        return code, text 

    def fmgr_copy(self, fops, notifyurl=None, separate=None):
        url = '{0}/fmgr/copy'.format(self.host)
        data = {'fops': fops}
        if notifyurl is not None:
            data['notifyURL'] = urlsafe_base64_encode(notifyurl)
        if separate is not None:
            data['separate'] = separate
        reqdata = self.params_parse(data)
        debug('Fmgr_copy request body is: %s' % reqdata)
        debug('Start to copy file')
        code, text = _post(url=url, data=reqdata,headers=self.gernerate_headers(url, body=reqdata))
        debug('The return code : %d, persistentId/test : %s' % (code, text))
        return code,text 
   
    def fmgr_fetch(self, fops, notifyurl=None, force=None, separate=None):
        url = '{0}/fmgr/fetch'.format(self.host)
        data = {'fops': fops}
        if notifyurl is not None:
            data['notifyURL'] = urlsafe_base64_encode(notifyurl)
        if force is not None:
            data['force'] = force
        if separate is not None:
            data['separate'] = separate
        reqdata = self.params_parse(data)
        debug('fmgr_fetch request body is: %s' % (reqdata))
        debug('Start to fetch file')
        code, text = _post(url=url, data=reqdata,headers=self.gernerate_headers(url, body=reqdata))
        debug('The return code : %d, ersistentId/text : %s' % (code, text))
        return code,text

    def fmgr_delete(self, fops, notifyurl=None, separate=None):
        url = '{0}/fmgr/delete'.format(self.host)
        data = {'fops': fops}
        if notifyurl is not None:
            data['notifyURL'] = urlsafe_base64_encode(notifyurl)
        if separate is not None:
            data['separate'] = separate
        reqdata = self.params_parse(data)
        debug('Fmgr_delete request body is: %s' % reqdata)
        debug('Start to superdelete operation')
        code, text = _post(url=url, data=reqdata,headers=self.gernerate_headers(url, body=reqdata))
        debug('The return code : %d, persistentId/text : %s' % (code, text))
        return code,text

    def prefix_delete(self, fops, notifyurl=None, separate=None):
        url = '{0}/fmgr/deletePrefix'.format(self.host)
        data = {'fops': fops}
        if notifyurl is not None:
            data['notifyURL'] = urlsafe_base64_encode(notifyurl)
        if separate is not None:
            data['separate'] = separate
        reqdata = self.params_parse(data)
        debug('DeletePrefix request body is: %s' % reqdata)
        debug('Start to deletePrefix operation')
        code, text = _post(url=url, data=reqdata,headers=self.gernerate_headers(url, body=reqdata))
        debug('The return code : %d, persistentId/text : %s' % (code, text))
        return code,text

    def m3u8_delete(self, fops, notifyurl=None, separate=None):
        url = '{0}/fmgr/deletem3u8'.format(self.host)
        data = {'fops': fops}
        if notifyurl is not None:
            data['notifyURL'] = urlsafe_base64_encode(notifyurl)
        if separate is not None:
            data['separate'] = separate
        reqdata = self.params_parse(data)
        debug('Deletem3u8 request body is: %s' % reqdata)
        debug('Start to deletem3u8 operation')
        code, text = _post(url=url, data=reqdata,headers=self.gernerate_headers(url, body=reqdata))
        debug('The return code : %d, persistentId/text : %s' % (code, text))
        return code,text
   
    def status(self, persistentId):
        url = '{0}/fmgr/status?persistentId={1}'.format(self.host, persistentId)
        debug('Start to get status of persistentId: %s' % persistentId)
        code, text = _get(url=url)
        debug('The return code : %d, text : %s' % (code, text))
        return code, text
