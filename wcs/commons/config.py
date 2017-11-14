# -*- coding: utf-8 -*-
import os
from wcs.commons.logme import debug,error
import re
import sys
import io

class Config(object):

    _instance = None
    _parsed_files = []
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
    # 是否断点续传
    upload_id = ''
 
    #可选参数output
    output = ''
    
    #可选参数notifyURL
    notifyurl = ''
    
    #可选参数separate
    separate = 0

    #可选参数force
    force = 0

    #bucket list可选参数limit
    limit = 1000
    prefix = ''
    mode = 1
    marker = ''

    #上传策略参数
    overwrite = 0
    returnUrl = ''
    returnBody = ''
    callbackUrl = ''
    callbackBody = ''
    persistentNotifyUrl = ''
    persistentOps = ''
    contentDetect = ''
    detectNotifyURL = ''
    detectNotifyRule = ''

    ## Creating a singleton
    def __new__(self, configfile=None, ak=None, sk=None, put_url=None, mgr_url=None ):
        if self._instance == None:
            self._instance = object.__new__(self)
        return self._instance

    def __init__(self, configfile=None):
        if configfile:
            try:
                self.read_config_file(configfile)
            except IOError as e:  # 这里尚未确定读取配置文件异常如何处理
                error("Can't read config file ")
                sys.exit()

    def option_list(self):
        retval = []
        funclist = ['option_list', 'read_config_file','dump_config','update_option']
        for option in dir(self):
            if option.startswith("_") or option in funclist:
                continue
            retval.append(option)
        return retval

    def read_config_file(self, configfile):
        cp = ConfigParser(configfile)
        for option in self.option_list():
            _option = cp.get(option)
            if _option is not None:
                _option = _option.strip()
            self.update_option(option, _option)
        self._parsed_files.append(configfile)

    def dump_config(self, stream):
        ConfigDumper(stream).dump(u"default", self)

    def update_option(self, option, value):
        if value is None:
            return
        if type(getattr(Config, option)) is type(True):
            if str(value).lower() in ("true","yes","on","1"):
                value = True
            elif str(value).lower() in ("false","no","off","0"):
                value = False
            else:
                raise ValueError("Config: value of option '%s' must be Yes or No, not '%s'" % (option, value))
        setattr(Config, option, value)

class ConfigParser(object):
    def __init__(self, file, sections = []):
        self.cfg = {}
        self.parse_file(file, sections)

    def parse_file(self, file, sections=[]):
        debug("ConfigParse: Reading file '%s'" % file)
        if type(sections) != type([]):
            sections = [sections]
        in_our_section = True
        r_section = re.compile("^\[([^\]]+)\]")
        r_comment = re.compile("^\s*#.*")
        r_empty = re.compile("\s*$")
        r_data = re.compile("^\s*(?P<key>\w+)\s*=\s*(?P<value>.*)")
        r_quotes = re.compile("^\"(.*)\"\s*$")
        with io.open(file, "r", encoding=self.get('encoding', 'UTF-8')) as fp:
            for line in fp:
                if r_comment.match(line) or r_empty.match(line):
                    continue
                is_section = r_section.match(line)
                if is_section:
                    section = is_section.group()[0]
                    in_our_section = (section in sections) or (len(sections) == 0)
                    continue
                is_data = r_data.match(line)
                if is_data and in_our_section:
                    data = is_data.groupdict()
                    if r_quotes.match(data["value"]):
                        data["value"] = data["value"][1:-1]
                    self.__setitem__(data["key"],data["value"])
                    if data["key"] in ("access_key","secret_key"):
                        print_value = ("%s...%d_chars...%s") % (data["value"][-2], len(data["value"]) - 3, data["value"][-1:1])
                    else:
                        print_value = data["value"]
                    debug("ConfigParser: %s->%s" % (data["key"], print_value))
                    continue
                warning("Ingnoring invalid line in '%s': %s" % (file, line))
    def __geteitem__(self, name):
        return self.cfg[name]

    def __setitem__(self, name, value):
        self.cfg[name] = value

    def get(self, name, default = None):
        if name in self.cfg:
            return self.cfg[name]
        return default

class ConfigDumper(object):
    def __init__(self, stream):
        self.stream = stream

    def dump(self, section, config):
        self.stream.write(u"[%s]\n" % section)
        for option in config.option_list():
            value = getattr(config, option)
            self.stream.write(u"%s = %s\n" % (option, value))
