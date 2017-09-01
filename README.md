# Python SDK使用指南
wcs-python-sdk从v1.0.0版本开始，SDK的功能包括：文件上传、资源管理、高级资源管理、持久化处理、相应操作状态查询以及直播录制文件查询。

此Python SDK适用于python 2.X和3.X环境，但是如果需要支持https，请将环境升级到2.7.9+再使用本SDK。

## 安装
推荐使用pip安装

* 直接安装

    > Python2: pip install wcs-python-sdk
    
    > Python3: pip3 install wcs-python-sdk-3
 

* 源码安装
    

    > tar xvzf wcs-python-sdk-$VERSION.tar.gz

    > cd wcs-python-sdk-$VERSION

    > python setup.py install


## 初始化
在使用SDK之前，您需要获得一对有效的AccessKey和SecretKey签名授权。

可以通过如下方法获得：

1. 开通网宿云存储账号
2. 登录网宿SI平台，在安全管理-秘钥管理查看AccessKey和SecretKey
3. 登录网宿SI平台，在安全管理-域名管理查看上传域名（puturl）和管理域名(mgrurl)。**如您使用的是http协议，最后的配置需添加http://前缀**

获取上面4个配置之后，调用如下代码进行初始化：

    from wcs.services.client import Client
    client = Client(Access_key, Secret_key, puturl, mgrurl)
    
## 计算文件etag值

wcs-python-sdk提供了计算文件etag值的工具，用户通过命令行的形式体验这个功能

    
    /usr/bin/wcs_etag_cal -h
    usage: WCS-Python-SDK [-h] {etag} ...
    
    positional arguments:
      {etag}
        etag      etag [file...]

    optional arguments:
     -h, --help  show this help message and exit

    /usr/bin/wcs_etag_cal etag filepath1 filepath2
    [filepath1, filepath2]
    FrA377uGHSxcTM62-rjsjvoKqRVS FiUsqBkZ6e8KaAA9Uu6q3qLPgmDW

常见问题

    在相应模块已经安装的情况下，使用工具时出现下面错误：
    pkg_resources.DistributionNotFound: [modulename]
    解决方案： 
    pip install --upgrade setuptools
    

## 上传文件

为了尽可能改善终端用户的上传体验，wcs-python-sdk提供了客户端直传功能，更多信息请参阅[wcs文档中心](https://wcs.chinanetcenter.com/document/API/FileUpload)

### 普通上传：

    from wcs.services.client import Client
    from wcs.commons.putpolicy import PutPolicy

    client = Client(Access_key, Secret_key, put_url, mgr_url)
  
    # 设定上传策略
    policy = PutPolicy()
    policy.set_conf('scope','%s:%s' % (bucket,key))
    .... 
    
    # 文件上传
    filepath = ''
    client.simple_upload(filepath,policy)
   
### 回调上传

    from wcs.services.client import Client
    from wcs.commons.putpolicy import PutPolicy

    client = Client(Access_key, Secret_key, put_url, mgr_url)
    
    # 设定上传策略，上传策略中设定了回调url以及callbackbody
    policy = PutPolicy()
    policy.set_conf('scope','%s:%s' % (bucket,key)
    policy.set_conf('callbackUrl',{callback})
    policy.set_conf('callbackBody','bucket=$(bucket)&key=$(key)')
    ....

    # 文件上传
    filepath = ''
    client.simple_upload(filepath,policy)
     
        
### 通知上传

    # 以图片加水印为例
    from wcs.services.client import Client
    from wcs.commons.putpolicy import PutPolicy

    client = Client(Access_key, Secret_key, put_url, mgr_url)
    
    # 设定上传策略，上传策略中设定了回调url以及callbackbody
    policy = PutPolicy()
    policy.set_conf('scope','%s:%s' % (bucket,key)
    ops = 'watermark/png/mode/1/dissolve/50|saveas/bHVtai10ZXN0OnF3YXItZm9wcw=='
    policy.set_conf('persistentOps',ops)
    policy.set_conf('persistentNotifyUrl', {notify})
    policy.set_conf('returnBody','key=$(key)&persistentId=$(persistentId)&fsize=$(fsize)')
    ....

    # 文件上传
    filepath = ''
    client.simple_upload(filepath,policy)

转码操作具体参数请参阅[ops参数格式](https://wcs.chinanetcenter.com/document/API/Appendix/fopsParam)；saveas为转码后文件另存为指定文件，参数中需要填入"空间:文件名"[URL安全的Base64编码](https://wcs.chinanetcenter.com/document/API/Appendix/UrlsafeBase64)后的值。

由此可知，上传成功后的行为主要是由[上传凭证](https://wcs.chinanetcenter.com/document/API/Token/UploadToken)中的上传策略来指定，其中上传策略可以指定的行为不止这些，具体请参阅[上传策略](https://wcs.chinanetcenter.com/document/API/Token/UploadToken#上传策略数据)


### 流地址上传

用户在上传文件时，提交文件的流地址，SDK通过流地址获取文件二进制流，然后通过mulitpart/form形式上传

**范例：** 

    from wcs.services.client import Client
    from wcs.commons.putpolicy import PutPolicy

    client = Client(Access_key, Secret_key, put_url, mgr_url)
  
    # 设定上传策略
    policy = PutPolicy()
    policy.set_conf('scope','%s:%s' % (bucket,key))
    .... 
    
    # 流地址上传
    stream = ''
    client.simple_upload(stream,policy)


### 分片上传

当文件大小超过500MB建议用户采用分片上传接口，具体分片流程请参阅[分片上传](https://wcs.chinanetcenter.com/document/API/FileUpload/SliceUpload)

**范例：** 

    from wcs.services.client import Client
    from wcs.commons.putpolicy import PutPolicy

    client = Client(Access_key, Secret_key, put_url, mgr_url)
  
    # 设定上传策略
    policy = PutPolicy()
    policy.set_conf('scope','%s:%s' % (bucket,key))
    .... 
    
    # 文件上传
    filepath = ''
    param = '' #可选
    client.multipart_upload(filepath,policy，param)
   

## 资源管理

### 资源列举
该接口提供在云存储平台分批列举指定空间内的资源，列举条目数，指定前缀等详细参数说明见[列举资源](https://wcs.chinanetcenter.com/document/API/ResourceManage/list)

**范例：** 
    
    from wcs.services.client import Client

    # 设定参数
    bucket = ''
    limit =  #可选
    prefix =  #可选
    marker =  #可选
    mode =  #可选 
    client = Client(Access_key, Secret_key, put_url, mgr_url)
    client.list(bucket, prefix, marker, limit, mode)

### 文件删除
该接口提供在云存储平台上删除一个指定资源文件

**范例：** 

    from wcs.services.client import Client

    bucket = ''
    key = '' 
    client = Client(Access_key, Secret_key, put_url, mgr_url)
    client.delete(bucket, key)

### 获取文件信息
该接口用于在云存储平台上获取一个文件的信息描述，包括文件名，文件大小，文件的ETag信息，以MIME信息表达的文件类型，文件上传时间。

**范例：**   

    from wcs.services.client import Client

    # 设定参数
    bucket = ''
    key = '' 
    client = Client(Access_key, Secret_key, put_url, mgr_url)
    client.stat(bucket, key)
   
### 文件复制
该接口提供将指定资源复制为新命名资源。如果目标空间存在同名资源，不会覆盖。
 
    from wcs.services.client import Client

    srcbucket = ''
    srckey = '' 
    dstbucket = ''
    dstkey = ''
    client = Client(Access_key, Secret_key, put_url, mgr_url)
    client.copy(srcbucket, srckey,dstbucket,dstkey)

### 文件移动
该接口提供将指定资源移动为新命名资源。如果目标空间存在同名资源，不会覆盖。

**范例：**

    from wcs.services.client import Client

    # 设定参数
    srcbucket = ''
    srckey = '' 
    dstbucket = ''
    dstkey = ''
    client = Client(Access_key, Secret_key, put_url, mgr_url)
    client.move(srcbucket, srckey,dstbucket,dstkey)

### 设置文件过期时间

该接口支持用户设置文件的保存期限，超过设置的天数文件自动删除。

**范例：**

    from wcs.services.client import Client

    # 设定参数
    bucket = ''
    key = ''
    deadline = ''
    client = Client(Access_key, Secret_key, put_url, mgr_url)
    client.setdeadline(bucket, key, deadline)


### 文件解压缩
该接口提供在云存储平台对压缩包进行解压缩的功能。解压缩后在云存储上默认生成一个list文件，文件内容包含解压缩后的文件信息。


**范例：**

    from wcs.services.client import Client

    # 设定参数
    bucket = ''
    key = ''
    fops = 'decompression/zip'
    client = Client(Access_key, Secret_key, put_url, mgr_url)
    client.setdeadline(fops,bucket, key)

## 高级资源管理

### 文件移动
该接口提供将指定资源移动到另一个空间，或者在同一空间重命名。请求参数以如下格式组织，作为请求内容提交，请求参数定义详见[文件移动](https://wcs.chinanetcenter.com/document/API/Fmgr/move)
   
    from wcs.services.client import Client

    # 参数配置
    movefops = ''
    notifyurl = ''  #可选
    separate =    #可选

    # 文件移动
    client = Client(Access_key, Secret_key, put_url, mgr_url)
    client.fmgr_move(movefops, notifyurl, separate)

### 文件复制
该接口提供将指定资源复制为新命名资源。请求参数以如下格式组织，作为请求内容提交,请求参数定义详见[文件复制](https://wcs.chinanetcenter.com/document/API/Fmgr/copy)
    
    from wcs.services.client import Client

    # 参数配置
    copyfops = ''
    notifyurl = ''  #可选
    separate =    #可选

    # 文件复制
    client = Client(Access_key, Secret_key, put_url, mgr_url)
    client.fmgr_copy(copyfops, notifyurl, separate)

### 文件删除
该接口提供删除指定资源。请求参数以如下格式组织，作为请求内容提交，请求参数定义详见[文件删除](https://wcs.chinanetcenter.com/document/API/Fmgr/delete)
    
    from wcs.services.client import Client

    # 参数配置
    delops = ''
    notifyurl = ''  #可选
    separate =    #可选

    # 文件删除
    client = Client(Access_key, Secret_key, put_url, mgr_url)
    client.fmgr_copy(delfops, notifyurl, separate)

### 文件抓取
该接口提供从指定URL抓取资源，并存储到指定空间。请求参数以如下格式组织，作为请求内容提交，请求参数定义详见[抓取资源](https://wcs.chinanetcenter.com/document/API/Fmgr/fetch)

    from wcs.services.client import Client

    # 参数配置
    fetops = ''
    notifyurl = ''  #可选
    separate =    #可选

    # 文件抓取
    client = Client(Access_key, Secret_key, put_url, mgr_url)
    client.fmgr_fetch(fetfops, notifyurl, separate)

### 按前缀删除资源
该接口提供删除符合指定前缀的资源。请求参数以如下格式组织，作为请求内容提交，请求参数详见[前缀删除资源](https://wcs.chinanetcenter.com/document/API/Fmgr/deletePrefix)
    
    from wcs.services.client import Client

    # 参数配置
    preops = ''
    notifyurl = ''  #可选
    separate =    #可选

    # 文件按前缀删除
    client = Client(Access_key, Secret_key, put_url, mgr_url)
    client.prefix_delete(prefops, notifyurl, separate)


### 删除m3u8文件
该接口提供删除指定资源。请求参数以如下格式组织，作为请求内容提交，请求参数详见[删除m3u8文件](https://wcs.chinanetcenter.com/document/API/Fmgr/deletem3u8)
   
    from wcs.services.client import Client

    # 参数配置
    m3u8ops = ''
    notifyurl = ''  #可选
    separate =    #可选

    # 删除m3u8文件
    client = Client(Access_key, Secret_key, put_url, mgr_url)
    client.m3u8_delete(m3u8ops, notifyurl, separate)

### Fmgr任务查询
该接口提供查询Fmgr任务的执行情况。 

注：notifyURL收到的Fmgr任务通知内容的格式与该接口响应内容的格式一致。

    from wcs.services.client import Client

    # 参数配置
    persistentId = ''

    # 任务查询
    client = Client(Access_key, Secret_key, put_url, mgr_url)
    client.fmgr_status(persistentId)

## 持久化操作
该接口用于根据ops的定义对某个音视频文件进行持久化处理，ops参数定义方式见[ops参数格式](https://wcs.chinanetcenter.com/document/API/Appendix/fopsParam#音视频处理)

以视频截图为例：
   
    from wcs.services.client import Client

    # 参数配置
    bucket = ''
    key = ''
    ops = ''
    force =  #可选
    notifyurl = ''   #可选
    separate =    #可选

    # 持久化操作
    client = Client(Access_key, Secret_key, put_url, mgr_url)
    code,text = client.ops_execute(ops, bucket,key,notifyurl, separate)
    # 任务执行状态查询
    client.ops_status(text['persistentId'])

## 直播录制文件查询
该接口支持用户查询直播录制的文件列表。请求参数说明如下：

    参数        必填	描述
    channelname	是	直播流名。
    startTime	是	指定直播开始时间。格式为YYYYMMDDmmhhss。
    endTime	    是	指定直播结束时间。格式为YYYYMMDDmmhhss。结束时间不能小于开始时间，且与开始时间间隔不能超过7天。
    bucket	    是	指定空间。
    start	    否	指定起始位置，查询结果从该位置开始返回，如0、1、100 默认值为1，即从查询范围内的第一条记录开始返回。
    limit	    否	指定查询个数。不指定则查询所有记录。

****
接口调用实例：

   
    from wcs.services.client import Client

    # 参数配置
    channelname = ''
    startTime = ''
    endTime = ''
    bucket = ''
    start = '' #可选
    limit = '' #可选
       
    # 直播录制文件查询
    client.wslive_list(channelname,startTime,startTime, bucket,start,limit)
