#!/usr/bin/python
## -*- coding: utf-8 -*-

class MgrBase(object):
    """资源管理基类
    资源管理类接口有很多相似的部分，为了降低代码冗余，将公共部分写入基类，需要时继承基类即可
    Attributes:
        auth: 上传&管理token计算实例
        mgr_host: 管理域名
    """
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

