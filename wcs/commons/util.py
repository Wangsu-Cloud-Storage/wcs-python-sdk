# -*- coding: utf-8 -*-
from hashlib import sha1
from base64 import urlsafe_b64encode, urlsafe_b64decode
import base64
import os
import logging
from .compat import b, s
import tempfile
import random
import string
from .config import Config

try:
    import zlib
    binascii = zlib
except ImportError:
    zlib = None
    import binascii


def urlsafe_base64_encode(data):
    """urlsafe的base64编码:
    对提供的数据进行urlsafe的base64编码。规格参考：
    Args:
        data: 待编码的数据，一般为字符串
    Returns:
        编码后的字符串
    """
    ret = urlsafe_b64encode(b(data))
    return s(ret)


def urlsafe_base64_decode(data):
    """urlsafe的base64解码:
    对提供的urlsafe的base64编码的数据进行解码
    Args:
        data: 待解码的数据，一般为字符串
    Returns:
        解码后的字符串。
    """
    ret = urlsafe_b64decode(s(data))
    return ret


def file_crc32(filePath):
    """计算文件的crc32检验码:
    Args:
        filePath: 待计算校验码的文件路径
    Returns:
        文件内容的crc32校验码。
    """
    crc = 0
    with open(filePath, 'rb') as f:
        for block in _file_iter(f,Config.block_size):
            crc = binascii.crc32(block, crc) & 0xFFFFFFFF
    return crc


def crc32(data):
    """计算输入流的crc32检验码:
    Args:
        data: 待计算校验码的字符流
    Returns:
        输入流的crc32校验码。
    """
    return binascii.crc32(b(data)) & 0xffffffff


def _file_iter(input_stream, offset,size):
    """读取输入流:
    Args:
        input_stream: 待读取文件的二进制流
        size:         二进制流的大小
    Raises:
        IOError: 文件流读取失败
    """
    input_stream.seek(offset)
    d = input_stream.read(size)
    while d :
        yield d
        d = input_stream.read(size)

def readfile(input,offset,size):
    input.seek(offset)
    d = input.read(size)
    if d:
        return d

def file_to_stream(path):
    return open(path, "rb")

def _sha1(data):
    """单块计算hash:
    Args:
        data: 待计算hash的数据
    Returns:
        输入数据计算的hash值
    """
    h = sha1()
    h.update(data)
    return h.digest()


def etag_stream(input_stream):
    """计算输入流的etag:
    Args:
        input_stream: 待计算etag的二进制流
    Returns:
        输入流的etag值
    """
    array = [_sha1(block) for block in _file_iter(input_stream, 0, Config.block_size)]
    if len(array) == 0:
        array = [_sha1(b'')]
    if len(array) == 1:
        data = array[0]
        prefix = b'\x16'
    else:
        sha1_str = b('').join(array)
        data = _sha1(sha1_str)
        prefix = b'\x96'
    return urlsafe_base64_encode(prefix + data)


def etag(filePath):
    """计算文件的etag:
    Args:
        filePath: 待计算etag的文件路径
    Returns:
        输入文件的etag值
    """
    with open(filePath, 'rb') as f:
        return etag_stream(f)


def entry(bucket, key):
    """计算wcs API中的数据格式:
    Args:
        bucket: 待操作的空间名
        key:    待操作的文件名
    Returns:
        符合wcs API规格的数据格式
    """
    if key is None:
        return urlsafe_base64_encode('{0}'.format(bucket))
    else:
        return urlsafe_base64_encode('{0}:{1}'.format(bucket, key))

def GetUuid():
    chars = string.ascii_letters+string.digits
    return ''.join([random.choice(chars) for i in range(32)])

def https_check(url):
    if Config.ishttps:
        return "https://" + url
    else:
        return "http://" + url
