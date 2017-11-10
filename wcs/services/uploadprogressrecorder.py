# -*- coding: utf-8 -*-

import base64
import json
import os
import tempfile
from lockfile import LockFile
from wcs.commons.config import Config

tmp_record_folder = Config.tmp_record_folder

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

    def get_upload_record(self, upload_id):
        upload_record_file_path = os.path.join(self.record_folder,upload_id)
        if not os.path.isfile(upload_record_file_path):
            return None
        with open(upload_record_file_path, 'r') as f:
            results = f.read()
        return eval(results)

    def set_upload_record(self, upload_id, data):
        upload_record_file_path = os.path.join(self.record_folder,upload_id)
        lock = LockFile(upload_record_file_path)
        lock.acquire()
        with open(upload_record_file_path, 'w') as f:
            json.dump(data, f)
            f.write("\n")
        lock.release()

    def delete_upload_record(self, upload_id):
        record_file_path = os.path.join(self.record_folder, upload_id)
        os.remove(record_file_path)

    def find_upload_record(self, upload_id):
        path = os.path.join(self.record_folder,upload_id)
        return os.path.isfile(path)
          
