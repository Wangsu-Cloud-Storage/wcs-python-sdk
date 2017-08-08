# -*- coding: utf-8 -*-

import base64
import json
import os
import tempfile
from lockfile import LockFile
from wcs.commons.config import tmp_record_folder


class UploadProgressRecorder(object):
    """持久化上传记录类
    该类默认保存每个文件的上传记录到文件系统中，用于断点续传
    上传记录为json格式：
    {
        "size": file size,
        "uploadBatch": slice upload task ID,
        "offset": position of block,
        "ctx": contexts
    }
    Attributes:
        record_folder: 保存上传记录的目录
    """
    def __init__(self):
        if tmp_record_folder is not None:
            if os.path.exists(tmp_record_folder) is False:
                os.mkdir(tmp_record_folder)
            self.record_folder = tmp_record_folder
        else:
            raise Exception("tmp_record_folder is necessary!")

    def get_upload_record(self, key):
        record_file_name = base64.b64encode(key.encode('utf-8')).decode('utf-8')
        upload_record_file_path = os.path.join(self.record_folder, record_file_name)
        if not os.path.isfile(upload_record_file_path):
            return None
        results = []
        with open(upload_record_file_path, 'r') as f:
            for line in f:
                results.append(eval(line))
        return results

    def set_upload_record(self, key, data):
        record_file_name = base64.b64encode(key.encode('utf-8')).decode('utf-8')
        upload_record_file_path = os.path.join(self.record_folder, record_file_name)
        lock = LockFile(upload_record_file_path)
        lock.acquire()
        with open(upload_record_file_path, 'a') as f:
            json.dump(data, f)
            f.write("\n")
        lock.release()

    def delete_upload_record(self, key):
        record_file_name = base64.b64encode(key.encode('utf-8')).decode('utf-8')
        record_file_path = os.path.join(self.record_folder, record_file_name)
        os.remove(record_file_path)
