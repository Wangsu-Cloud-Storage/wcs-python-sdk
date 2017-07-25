# -*- coding: utf-8 -*-
MGR_URL = 'jsij'
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

