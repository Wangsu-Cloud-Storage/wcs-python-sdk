
class MgrBase(object):

    def __init__(self, auth,mgr_url):
        self.auth = auth
        self.mgr_host = mgr_url

    def _gernerate_headers(self,url,body=None):
        token = self.auth.managertoken(url,body=body)
        headers = {'Authorization': token}
        return headers
        
    def _params_parse(self, params):
        if params:
            paramlist = [] 
            for k, v in params.items():
                paramlist.append('{0}={1}'.format(k, v))
            paramlist = '&'.join(paramlist) 
        return paramlist

