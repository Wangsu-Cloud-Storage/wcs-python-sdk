import os
import requests
from requests_toolbelt import MultipartEncoder
from wcs.commons.http import _post
from wcs.commons.logme import debug,error
from wcs.commons.util import https_check

class SimpleUpload(object):

    def __init__(self,url):
        self.url = url

    def _gernerate_tool(self, f,token):
        fileds = {"token":token}
        url = "{0}/{1}/{2}".format(self.url,"file","upload")
        fileds['file'] = ('filename', f, 'text/plain')
        encoder = MultipartEncoder(fileds)
        headers = {"Content-Type":encoder.content_type}
        headers['user-agent'] = "WCSCMD-1.0.0(http://wcs.chinanetcenter.com)"
        return url, encoder, headers  
    
    def _gernerate_content(self,path):
        return open(path, 'rb')

    def _upload(self,url,encoder,headers,f):
        url = https_check(url)
        try:
            r = requests.post(url=url, headers=headers, data=encoder, verify=True)
        except Exception as e:
            f.close()
            debug('Request url:' + url)
            debug('Headers:')
            debug(headers)
            debug('Exception:')
            debug(e)
            return -1,e
        f.close()
        debug('Status Code:' + str(r.status_code))
        debug('Response Body:')
        debug(r.text)
        return r.status_code,r.text

    def upload(self, filepath,token):
        if os.path.exists(filepath) and os.path.isfile(filepath):
            f = self._gernerate_content(filepath)
            url,encoder,headers = self._gernerate_tool(f,token)
            return self._upload(url,encoder,headers,f)
        else:
            error('Sorry ! Please input a existing file')
            raise ValueError("Sorry ! We need a existing file to upload")
