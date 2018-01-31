import ast
import os
from os.path import expanduser
try:
    import simplejson as json
except (ImportError, SyntaxError):
    # simplejson does not support Python 3.2, it thows a SyntaxError
    # because of u'...' Unicode literals.
    import json  # noqa
import platform
import requests
from .config import Config
from requests.adapters import HTTPAdapter
import yaml

_session = None
config_file = os.path.join(expanduser("~"), ".wcscfg")
cfg = Config(config_file)
timeout = float(cfg.connection_timeout)

def __return_wrapper(resp):
    if resp.text != '':
        resp_header = {'x-reqid': resp.headers['x-reqid']}
        try:
            return resp.status_code, eval(str(resp.text)), resp_header
        except Exception as e:
            response_body = yaml.load(resp.text)
            if 'code' in response_body.keys():
                return response_body["code"],response_body,resp_header
            else:
                return -2, {'message':resp.text}, resp_header
    else:
        return -2, {'message':'Message Body is None. Please check your URL.'}, resp_header
        

def _init():
    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=Config.connection_retries))
    global _session
    _session = session


def _post(url, headers, data=None, files=None):
    if _session is None:
        _init()
    try:
        headers['user-agent'] = 'WCS-Python-SDK-4.0.0(http://wcs.chinanetcenter.com)'
        #headers['Expect'] = '100-conitnue'
        r = requests.post(url=url, data=data, files=files, headers=headers, timeout=timeout, verify=True)
    except Exception as e:
        return -1,e,'Null'
    return __return_wrapper(r)

def _get(url, headers=None):
    try:
        headers = headers or {}
        headers['user-agent'] = 'WCS-Python-SDK-4.0.0(http://wcs.chinanetcenter.com)'
        r = requests.get(url, headers=headers, timeout=timeout, verify=True)
    except Exception as e:
        return -1,e,'Null'
    return __return_wrapper(r)

