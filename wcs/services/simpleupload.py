#!/usr/bin/python
## -*- coding: utf-8 -*-

import os
from os.path import expanduser
import urllib
import requests
from requests_toolbelt import MultipartEncoder
from wcs.commons.config import Config
from wcs.commons.logme import debug,error
from wcs.commons.util import https_check
from requests.adapters import HTTPAdapter
from wcs.commons.config import Config
from wcs import __version__
#config_file = os.path.join(expanduser("~"), ".wcscfg")

class SimpleUpload(object):
    """普通上传类
    该类实现了WCS的普通上传功能
    Attributes:
        url: 上传域名    
    """

    def __init__(self,url):
        self.url = url
        session = requests.Session()
        session.mount('http://', HTTPAdapter(max_retries=int(Config.connection_retries)))
        session.mount('https://', HTTPAdapter(max_retries=int(Config.connection_retries)))
        global _session
        _session = session
        #self.cfg = Config(config_file)
        self.cfg = Config()

    def _gernerate_tool(self, f,token ,key):
        fileds = {"token":token}
        url = "{0}/{1}/{2}".format(self.url,"file","upload")
        fileds['file'] = (urllib.quote(key.encode('utf-8')), f, 'text/plain')
        encoder = MultipartEncoder(fileds)
        headers = {"Content-Type":encoder.content_type}
        headers['Expect'] = '100-continue'
        headers['user-agent'] = "WCS-Python-SDK-{0}(http://wcs.chinanetcenter.com)".format(__version__)
        try:
            if int(self.cfg.traffic_limit):
                headers['x-wos-traffic-limit'] = '{0}'.format(self.cfg.traffic_limit)
        except Exception as e:
            raise ValueError('traffic_limit parameter configuration error：{0}'.format(self.cfg.traffic_limit))
        m = encoder.to_string()
        return url, m, headers

    def _gernerate_content(self, path):
        return open(path, 'rb')

    def _upload(self,url,encoder,headers,f):

        url = https_check(url)
        if self.cfg.keepalive == True:
            pass
        else:
            _session.keep_alive = False
            headers['Connection'] = 'close'
        try:
            if self.cfg.isverify:
                if self.cfg.returnUrl:
                    r = _session.post(url=url, headers=headers, data=encoder, verify=True,allow_redirects=False)
                else:
                    r = _session.post(url=url, headers=headers, data=encoder, verify=True)
            else:
                if self.cfg.returnUrl:
                    r = _session.post(url=url, headers=headers, data=encoder, verify=False,allow_redirects=False)
                else:
                    r = _session.post(url=url, headers=headers, data=encoder, verify=False)
        except requests.ConnectionError as conn_error:
            debug('Url connection abnormal,please check url!')
            return -1,conn_error
        except Exception as e:
            f.close()
            debug('Request url:' + url)
            debug('Headers:')
            debug(headers)
            debug('Exception:')
            debug(e)
            return -1,e
        f.close()
        try:
            r_header = {'x-reqid': r.headers['x-reqid']}
            if r.status_code == 303:
                return r.status_code, r.headers['Location'], r_header
            else:
                return r.status_code, r.text, r_header
        except:
            return r.status_code,r.text

    def upload(self, filepath,token ,key='filename'):
        if os.path.exists(filepath) and os.path.isfile(filepath):
            f = self._gernerate_content(filepath)
            url,encoder,headers = self._gernerate_tool(f,token ,key)
            return self._upload(url,encoder,headers,f)
        else:
            error('Sorry ! Please input a existing file')
            raise ValueError("Sorry ! We need a existing file to upload")
