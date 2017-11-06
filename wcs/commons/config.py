# -*- coding: utf-8 -*-
import os

class Config(object):

    _instance = None
    access_key = ''
    secret_key = ''
    put_url = ''
    mgr_url = ''
    # 设置分片上传的块大小和片大小，单位均为字节
    block_size = 1024 * 1024 * 4
    bput_size = 512 * 1024

    # 设置请求连接超时重传次数
    connection_retries = 3
    connection_timeout = 40

    # 设置重传失败重试次数
    mkblk_retries = 3
    bput_retries = 3
    mkfile_retries = 3

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

    def __init__(self, configfile=None):
        if configfile:
            try:
                self.read_config_file(configfile)
            except IOError as e:  # 这里尚未确定读取配置文件异常如何处理
                raise("Can't read config file %s for reason" % (configfile, e) )

    def read_config_file(self, configfile):
        pass

    def dump_config(self, stream):
        pass
