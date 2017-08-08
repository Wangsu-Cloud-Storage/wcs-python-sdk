# -*- coding: utf-8 -*-

# 设置管理域名 & 上传域名
PUT_URL = 'http://'
MGR_URL = 'http://'

# 设置分片上传的块大小和片大小，单位均为字节
_BLOCK_SIZE = 1024 * 1024 * 4
_BPUT_SIZE = 512 * 1024

# 设置请求连接超时重传次数
connection_retries = 3
connection_timeout = 40

# 设置重传失败重试次数
mkblk_retries = 3
bput_retries = 3
mkfile_retries = 3

# 设置日志存储路径
logging_folder = '/tmp/logger/'

# 设置分片上传过程中的上传记录存储路径
tmp_record_folder = '/tmp/sliceupload/'

# 设置分片上传并发线程数
# 如果留空，默认为机器的CPU核数，但是考虑带宽问题，一般设为<=计算机核数
Thread_num = 4

class PutPolicy(object):
    
    def __init__(self):
        
        self.putpolicy = {}
        self.policy = set(['scope','deadline','saveKey','fsizeLimit','overwrite','returnUrl','returnBody','callbackUrl','callbackBody','persistentNotifyUrl','persistentOps','separate','instant'])

    def set_conf(self, key, value):
        
        if key in self.policy:
            self.putpolicy[key] = value
        else:
            print ("invalid putpolicy param\n")
    
    def get_conf(self, key):
  
        if key in self.policy:
            return key + ":" + self.putpolicy[key]
        else:
            print ("invalid putpolicy param\n")

