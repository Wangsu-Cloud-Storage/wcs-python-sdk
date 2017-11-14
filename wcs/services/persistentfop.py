from wcs.services.mgrbase import MgrBase
from wcs.commons.config import Config
from wcs.commons.http import _post
from wcs.commons.http import _get
from wcs.commons.util import urlsafe_base64_encode

from wcs.commons.logme import debug, error

MGR_URL = Config.mgr_url

class PersistentFop(MgrBase):

    def __init__(self,auth,url):
        super(PersistentFop, self).__init__(auth,url)
      
    def _build_op(self,cmd, first_arg, **kwargs):
        op = [cmd]
        if first_arg is not None:
            op.append(first_arg)

        for k, v in kwargs.items():
            op.append('{0}/{1}'.format(k, v))
        return '/'.join(op)

    def _pipe_cmd(self,*cmds):
        return '|'.join(cmds)

    def _op_save(self,op, bucket, key):
        return _pipe_cmd(op, 'saveas/' + entry(bucket, key))

    def build_ops(self,ops,bucket,key):
        ops_list = []
        for op,params in ops.items(): 
            ops_list.append(self._op_save(self._build_op(op,params),bucket,key))
        return ops_list

    def fops_status(self, persistentId):
        url = '{0}/status/get/prefop?persistentId={1}'.format(self.mgr_host, persistentId)
        debug('Start to get status of persistentId: %s' % persistentId)
        code, text = _get(url=url)
        debug('The return code and text of status request is:%d %s' % (code, text))
        return code, text

    def _gernerate_headers(self,url,data):
        reqdata = super(PersistentFop, self)._params_parse(data)
        headers = super(PersistentFop, self)._gernerate_headers(url, body=reqdata) 
        return headers,reqdata

    def execute(self,fops,bucket,key,force=None,separate=None,notifyurl=None):
        data = {'bucket': urlsafe_base64_encode(bucket), 'key': urlsafe_base64_encode(key), 'fops': urlsafe_base64_encode(fops)}
        if notifyurl is not None:
            data['notifyURL'] = urlsafe_base64_encode(notifyurl)
        if force == 1:
            data['force'] = 1
        if separate == 1:
            data['separate'] = 1
        url = '{0}/fops'.format(self.mgr_host)
        headers,reqdata = self._gernerate_headers(url,data)
        debug('PersistentFops is %s' % fops)
        debug('Start to post persistentFops')
        return _post(url=url, data=reqdata,headers=headers)


