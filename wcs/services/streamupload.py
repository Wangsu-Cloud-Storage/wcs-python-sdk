import requests
from io import BytesIO
from requests_toolbelt import MultipartEncoder

from wcs.commons.config import PUT_URL
from wcs.commons.config import logging_folder
from wcs.commons.logme import debug, warning, error

class StreamUpload(object):
    
    def __init__(self, uploadtoken):
        self.fileds = {"token":uploadtoken}

    def upload(self, stream):
        memory = BytesIO()
        file = requests.get(stream)
        memory.write(file.content)
        debug('Stream file size is %d' % len(file.content))
        puturl = "{0}/{1}/{2}".format(PUT_URL,"file","upload")
        self.fileds["file"] = ('filename', memory,'text/plain')
        
        encoder = MultipartEncoder(self.fileds)
        headers = {"Content-Type":encoder.content_type}
        
        try:
            debug("Stream file %s upload start !" % stream)
            r = requests.post(url=puturl, headers=headers, data=encoder, verify=True)
        except Exception as e:
            debug("Exception: %s" % e)
            memory.close()
            return -1, e
        memory.close()
        debug("The result of upload is: %d %s" % (r.status_code, r.text))
        return r.status_code, r.text
        
