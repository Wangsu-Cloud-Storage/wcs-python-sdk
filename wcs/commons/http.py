#!/usr/bin/python
## -*- coding: utf-8 -*-

import ast
import os
from os.path import expanduser
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
try:
    import simplejson as json
except (ImportError, SyntaxError):
    # simplejson does not support Python 3.2, it thows a SyntaxError
    # because of u'...' Unicode literals.
    import json  # noqa
import platform
import requests
from wcs.commons.config import Config
from requests.adapters import HTTPAdapter
import yaml
#config_file = os.path.join(expanduser("~"), ".wcscfg")
from wcs import __version__
_session = None
def __return_wrapper(resp):
    try:
        if resp.text != '':
            if 'X-Reqid' in resp.headers.keys():
                resp_header = {'x-reqid': resp.headers['X-Reqid']}
            else:
                resp_header = {'x-reqid': 'None'}
            try:
                return resp.status_code, json.loads(str(resp.text)), resp_header
            except Exception as e:
                response_body = yaml.load(resp.text)
                if 'code' in response_body.keys():
                    return response_body["code"],response_body,resp_header
                else:
                    return -2, {'message':resp.text}, resp_header
        else:
            if resp.status_code == 303:
                resp_header = {'x-reqid': resp.headers['X-Reqid']}
                return resp.status_code, resp.headers['Location'], resp_header
            resp_header = resp.headers
            return -2, {'message':'Message Body is None. Please check your URL.'}, resp_header
    except Exception as e:
        return -2, {'message':'Some abnormal error occurred on the server.'}, {'x-reqid': 'None'}

def _init():
    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=int(Config.connection_retries)))
    session.mount('https://', HTTPAdapter(max_retries=int(Config.connection_retries)))
    global _session
    _session = session


def _post(url, headers, data=None, files=None):
    #cfg = Config(config_file)
    cfg = Config()
    timeout = float(cfg.connection_timeout)
    if _session is None:
        _init()
    try:
        headers['user-agent'] = 'WCS-Python-SDK-{0}(http://wcs.chinanetcenter.com)'.format(__version__)
        #headers['Expect'] = '100-conitnue'
        if cfg.keepalive == True:
            pass
        else:
            _session.keep_alive = False
            headers['Connection'] = 'close'
        if cfg.isverify:
            if cfg.returnUrl:
                r = _session.post(url=url, data=data, files=files, headers=headers, timeout=timeout, verify=True, allow_redirects=False)
            else:
                r = _session.post(url=url, data=data, files=files, headers=headers, timeout=timeout, verify=True)
        else:
            if cfg.returnUrl:
                r = _session.post(url=url, data=data, files=files, headers=headers, timeout=timeout, verify=False, allow_redirects=False)
            else:
                r = _session.post(url=url, data=data, files=files, headers=headers, timeout=timeout, verify=False)
    except Exception as e:
        errormessage = {'message':str(e)}
        return -1,errormessage,'None'
    return __return_wrapper(r)

def _get(url, headers=None):
    #cfg = Config(config_file)
    cfg = Config()
    timeout = float(cfg.connection_timeout)
    if _session is None:
        _init()
    try:
        headers = headers or {}
        headers['user-agent'] = 'WCS-Python-SDK-{0}(http://wcs.chinanetcenter.com)'.format(__version__)
        if cfg.keepalive == True:
            pass
        else:
            _session.keep_alive = False
            headers['Connection'] = 'close'
        if cfg.isverify:
            r = _session.get(url, headers=headers, timeout=timeout, verify=True)
        else:
            r = _session.get(url, headers=headers, timeout=timeout, verify=False)
    except Exception as e:
        resp_header = {'x-reqid': 'None'}
        return -1,e,resp_header
    return __return_wrapper(r)
