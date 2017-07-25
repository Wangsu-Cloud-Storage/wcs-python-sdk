import ast
try:
    import simplejson as json
except (ImportError, SyntaxError):
    # simplejson does not support Python 3.2, it thows a SyntaxError
    # because of u'...' Unicode literals.
    import json  # noqa
import platform
import requests
from .config import connection_retries
from .config import connection_timeout
from requests.adapters import HTTPAdapter

_session = None

def __return_wrapper(resp):
    if resp.text != '':
        try:
            return resp.status_code, eval(str(resp.text))
        except Exception as e:
            return resp.status_code, {'message':resp.text}
    else:
        return -1, {'message':'Message Body is None. Please check your URL.'}
        

def _init():
    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=connection_retries))
    global _session
    _session = session


def _post(url, headers, data=None, files=None):
    null =''
    true= 'true'
    false='false'
    if _session is None:
        _init()
    try:
        r = requests.post(url=url, data=data, files=files, headers=headers, timeout=connection_timeout, verify=True)
    except Exception as e:
        return -1,e
    return __return_wrapper(r)

def _get(url, headers=None,data=None):
    null =''
    true= 'true'
    false='false'
    try:
        r = requests.get(url, data=data,timeout=connection_timeout, headers=headers, verify=True)
    except Exception as e:
        return -1,e
    return __return_wrapper(r)

