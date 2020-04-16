#!/usr/bin/python
## -*- coding: utf-8 -*-
from io import BytesIO

import requests
from wcs.services.simpleupload import SimpleUpload


class StreamUpload(SimpleUpload):
    """流地址上传类
    该类继承自普通上传类，用于流地址上传，与普通上传相比差别是源数据来源于一个公网URL由URL获取到数据内容之后，不是落盘而是写入内存，再调用普通上传API完成上传
    """   
    def __init__(self, url):
        super(StreamUpload, self).__init__(url)

    def _gernerate_content(self, stream):
        memory = BytesIO()
        file = requests.get(stream)
        memory.write(file.content)
        return memory

    def upload(self, stream,token ,key):
        memory = self._gernerate_content(stream)
        url,encoder,headers = super(StreamUpload, self)._gernerate_tool(memory,token,key)
        return super(StreamUpload,self)._upload(url,encoder,headers,memory)
