# -*- coding: utf-8 -*-
import os

class Config(object):

    _instance = None
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

    # 记录分片上传进度
    tmp_record_folder = '/tmp/multipart/'

    # 设置分片上传并发线程数
    # 如果留空，默认为机器的CPU核数，但是考虑带宽问题，一般设为<=计算机核数
    concurrency = 4
    # 是否支持https
    ishttps = False

    ## Creating a singleton
    def __new__(self, configfile=None, ak=None, sk=None, put_url=None, mgr_url=None ):
        if self._instance = None:
            self._instance = object.__new__(self)
        return self._instance

    def __init__(self, configfile=None, ak=None, sk=None, put_url=None, mgr_url=None):
        if configfile:
            try:
                self.read_config_file(configfile)
            except IOError as e:  # 这里尚未确定读取配置文件异常如何处理
                raise("Can't read config file %s for reason" % (configfile, e) )

            if ak and sk:
                self.access_key = ak
                self.secret_key = sk

            if len(self.access_key) == 0:
                env_access_key = os.en