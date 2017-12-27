# -*- coding: utf-8 -*-

import base64
import json
import os,sys
import tempfile
import shutil
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
    def __init__(self,upload_id):
        tmp = tmp_record_folder + '/%s/' % upload_id
        if tmp is not None:
            if os.path.exists(tmp) is False:
                try:
                    os.makedirs(tmp)
                except Exception as e:
                    raise Exception('mkdir fail')
                    sys.exit()
            self.record_folder = tmp
            self.upload_id = upload_id
        else:
            raise Exception("tmp_record_folder is necessary!")

    def get_upload_record(self):
        results = {'uploadBatch':self.upload_id,'upload_record':[]}
        offsets = os.listdir(self.record_folder)
        if len(offsets) == 0:
            raise Exception('upload_records is Null, please redefine uploadBatch')
            sys.exit()
        for offset in offsets:
            path = os.path.join(self.record_folder, offset)
            try:
                with open(path, 'r') as f:
                    results['upload_record'].append(f.read())
            except Exception as e:
                raise Exception("Read upload progress fail")
                sys.exit()
        return results

    def set_upload_record(self, offset, data):
        upload_record_file_path = os.path.join(self.record_folder, str(offset))
        try:
            with open(upload_record_file_path, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            raise Exception('Write upload progress fail')
            sys.exit()

    def delete_upload_record(self):
        try:
            shutil.rmtree(self.record_folder)
        except Exception as e:
            raise Exception('Delete upload progress fail')
            sys.exit()

    def find_upload_record(self):
        return os.path.exists(self.record_folder)
          
