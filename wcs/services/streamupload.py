import requests
from io import BytesIO
from requests_toolbelt import MultipartEncoder

from wcs.services.simpleupload import SimpleUpload

class StreamUpload(SimpleUpload):
    
    def __init__(self, url):
        super(StreamUpload, self).__init__(url)

    def _gernerate_content(self, stream):
        memory = BytesIO()
        file = requests.get(stream)
        memory.write(file.content)
        return memory

    def upload(self, stream,token):
        memory = self._gernerate_content(stream)
        url,encoder,headers = super(StreamUpload, self)._gernerate_tool(memory,token)
        return super(StreamUpload,self)._upload(url,encoder,headers,memory)
