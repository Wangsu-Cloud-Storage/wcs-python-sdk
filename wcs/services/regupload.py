
import os
import requests
import sys
from requests_toolbelt import MultipartEncoder

from wcs.commons.config import PUT_URL
from wcs.commons.http import _post
from wcs.commons.util import urlsafe_base64_decode
from wcs.commons.config import logging_folder
from wcs.commons.logme import debug, warning, error


class RegUpload(object):

    def __init__(self,uploadtoken):
        self.fileds = {"token":uploadtoken}
        
    def reg_upload(self, filepath):
        puturl = "{0}/{1}/{2}".format(PUT_URL,"file","upload")
        if os.path.exists(filepath) and os.path.isfile(filepath):
            try:
                f = open(filepath, 'rb')
            except IOError as err:
                debug('IO Exception:%s' % err)
                return -1, err

            self.fileds["file"] = ('filename', f, 'text/plain')

            encoder = MultipartEncoder(self.fileds)
            headers = {"Content-Type":encoder.content_type}

            try:
                debug('File %s upload start!' % filepath)
                r = requests.post(url=puturl, headers=headers, data=encoder, verify=True)
            except Exception as e:
                debug('Post Exception:%s' % e)
                f.close()
                return -1, e
            f.close()
            debug('The result of upload is: %d, %s' % (r.status_code, r.text))
            return r.status_code, r.text
        else:
            error('Sorry ! Please input a existing file')
            raise ValueError("Sorry ! We need a existing file to upload")
