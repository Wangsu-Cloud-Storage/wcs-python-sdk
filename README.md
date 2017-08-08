# Python SDK使用指南
wcs-python-sdk从v1.0.0版本开始，SDK的功能包括：文件上传、资源管理、高级资源管理、持久化处理、相应操作状态查询以及直播录制文件查询。

此Python SDK适用于python 2.X和3.X环境，但是如果需要支持https，请将环境升级到2.7.9+再使用本SDK。

## 安装
* 直接安装

    > pip install wcs-python-sdk  
 

* 源码安装
    

    > tar xvzf wcs-python-sdk-$VERSION.tar.gz

    > cd wcs-python-sdk-$VERSION

    > python setup.py install


## 初始化
在使用SDK之前，您需要获得一对有效的AccessKey和SecretKey签名授权。

可以通过如下方法获得：

1. 开通网宿云存储账号
2. 登录网宿SI平台，在安全管理-秘钥管理查看AccessKey和SecretKey

获取AccessKey和SecretKey之后，调用如下两行代码进行初始化对接：

    from wcs.commons.auth import Auth
    auth =  Auth(AccessKey, SecretKey)
同时，需要在commons/config.py中对上传域名/管理域名、重传次数以及分片上传记录存储路径进行些必要的设置。 在使用sdk支持的服务过程中，可以在用户设置的日志存储目录下获得相应的日志记录，以监测本次操作的细节：

    # 设置管理域名 & 上传域名 
    PUT_URL = 'http://user.up0.v1.wcsapi.com' 
    MGR_URL = 'http://bucket.mgr0.v1.wcsapi.com'   
    
    # 设置分片上传的块大小和片大小，单位均为字节
    _BLOCK_SIZE = 1024 * 1024 * 4  
    _BPUT_SIZE = 512 * 1024 
    
    # 设置请求连接超时重传次数  
    connection_retries = 3   
    connection_timeout = 20 
   
    # 设置重传失败重试次数
    mkblk_retries = 3 
    bput_retries = 3
    mkfile_retries = 3  

    # 设置分片上传过程中的上传记录存储路径  
    tmp_record_folder = '/tmp/sliceupload/'
    
    # 设置日志存储路径
    logger_folder = '/tmp/logging/'  

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

    from wcs.services.regupload import RegUpload
    from wcs.commons.auth import Auth

    # 填写AccessKey和SecretKey
    access_key = ''
    secret_key = ''

    # 生成鉴权对象
    auth = Auth(access_key, secret_key)
    
    # 设定上传策略 & token
    putpolicy = {'scope':'bucket:key', 'deadline':'1475294400000'}
    token = auth.uploadtoken(putpolicy)
    
    # 要上传文件的本地路径
    localfile = ''

    # 文件上传
    regupload = RegUpload(token）
    code, text = regupload.reg_upload(localfile)
   
### 回调上传

    from wcs.services.regupload import RegUpload
    from wcs.commons.auth import Auth

    # 填写AccessKey和SecretKey
    access_key = ''
    secret_key = ''

    # 生成鉴权对象
    auth = Auth(access_key, secret_key)
    
    # 设定上传策略 & token，上传策略中设定了回调url以及callbackbody
    putpolicy = {'scope':'bucket:key', 'deadline':'1475294400000'，callbackUrl':callback,'callbackBody':'bucket=$(bucket)&key=$(key)'}
    token = auth.uploadtoken(putpolicy)
    
    # 要上传文件的本地路径
    localfile = ''

    # 文件上传
    regupload = RegUpload(token）
    code, text = regupload.reg_upload(localfile)
     
        
### 通知上传

    # 以图片加水印为例
    from wcs.services.regupload import RegUpload
    from wcs.commons.auth import Auth

    # 填写AccessKey和SecretKey
    access_key = ''
    secret_key = ''

    # 生成鉴权对象
    auth = Auth(access_key, secret_key)
    
    # 指令设定
    ops = 'watermark/png/mode/1/dissolve/50|saveas/bHVtai10ZXN0OnF3YXItZm9wcw=='
    
    # 设定上传策略 & token，上传策略中设定了回调url以及callbackbody
    putpolicy = {'scope':'bucket:key', 'deadline':'1475294400000'，'persistentNotifyUrl':notify,'persistentOps':ops,'overwrite':1,'returnBody':'key=$(key)&persistentId=$(persistentId)&fsize=$(fsize)'}
    token = auth.uploadtoken(putpolicy)
    
    # 要上传文件的本地路径
    localfile = ''

    # 文件上传
    regupload = RegUpload(token）
    code, text = regupload.reg_upload(localfile)

转码操作具体参数请参阅[ops参数格式](https://wcs.chinanetcenter.com/document/API/Appendix/fopsParam)；saveas为转码后文件另存为指定文件，参数中需要填入"空间:文件名"[URL安全的Base64编码](https://wcs.chinanetcenter.com/document/API/Appendix/UrlsafeBase64)后的值。

由此可知，上传成功后的行为主要是由[上传凭证](https://wcs.chinanetcenter.com/document/API/Token/UploadToken)中的上传策略来指定，其中上传策略可以指定的行为不止这些，具体请参阅[上传策略](https://wcs.chinanetcenter.com/document/API/Token/UploadToken#上传策略数据)


### 流地址上传

用户在上传文件时，提交文件的流地址，SDK通过流地址获取文件二进制流，然后通过mulitpart/form形式上传

    from wcs.services.streamupload import StreamUpload
    from wcs.commons.auth import Auth

    # 填写AccessKey和SecretKey
    access_key = ''
    secret_key = ''

    # 生成鉴权对象
    auth = Auth(access_key, secret_key)
    
    # 设定上传策略 & token，上传策略中设定了回调url以及callbackbody
    putpolicy = {'scope':'bucket:key', 'deadline':'1475294400000'}
    token = auth.uploadtoken(putpolicy)
    
    # 要上传文件的流地址
    stream = ''

    # 文件上传
    smupload = StreamUpload(token）
    code, text = smupload.upload(stream)


### 分片上传

当文件大小超过500MB建议用户采用分片上传接口，具体分片流程请参阅[分片上传](https://wcs.chinanetcenter.com/document/API/FileUpload/SliceUpload) ，

    import time
    from wcs.commons.auth import Auth
    from wcs.services.sliceupload import SliceUpload
    from wcs.services.uploadprogressrecorder import UploadProgressRecorder

    # 填写AccessKey和SecretKey
    access_key = ''
    secret_key = ''

    # 生成鉴权对象
    auth = Auth(access_key, secret_key)
    
    # 设定上传策略 & token
    putpolicy = {'scope':'bucket:key', 'deadline':'1475294400000'}
    token = auth.uploadtoken(putpolicy)
    
    # 要上传文件的本地路径
    localfile = ''
    # 设定mkfile参数
    param = {'position':'local','message':'upload'}
    # 记录上传进度
    upload_progress_recorder = UploadProgressRecorder()
    # 记录上传进度文件修改时间
    modify_time = time.time()
    
    # 文件上传
    sliceupload = SliceUpload(uploadtoken, bigfile, key, param, upload_progress_recorder, modify_time)
    code,hashvalue = sliceupload.slice_upload()
   

## 资源管理

### 资源列举
该接口提供在云存储平台分批列举指定空间内的资源，列举条目数，指定前缀等详细参数说明见[列举资源](https://wcs.chinanetcenter.com/document/API/ResourceManage/list)
    
    from wcs.commons.auth import Auth
    from wcs.services.filemanager import BucketManager
    
    # 填写AccessKey和SecretKey
    access_key = ''
    secret_key = ''

    # 生成鉴权对象
    auth = Auth(access_key, secret_key)
    
    # 资源列举
    filemanager = FileManager.bucketlist(auth, limit=100)
### 文件删除
该接口提供在云存储平台上删除一个指定资源文件

    from wcs.commons.auth import Auth
    from wcs.services.filemanager import BucketManager
    
    # 填写AccessKey和SecretKey
    access_key = ''
    secret_key = ''

    # 生成鉴权对象
    auth = Auth(access_key, secret_key)
    
    # 文件删除
    filemanager = FileManager(auth)
    code, text = filemanager.delete(bucket，key)

### 获取文件信息
该接口用于在云存储平台上获取一个文件的信息描述，包括文件名，文件大小，文件的ETag信息，以MIME信息表达的文件类型，文件上传时间。

    from wcs.commons.auth import Auth
    from wcs.services.filemanager import BucketManager
    
    # 填写AccessKey和SecretKey
    access_key = ''
    secret_key = ''

    # 生成鉴权对象
    auth = Auth(access_key, secret_key)
    
    # 获取文件信息
    filemanager = FileManager(auth)
    code, text = filemanager.stat(bucket，key)
   
### 文件复制
该接口提供将指定资源复制为新命名资源。如果目标空间存在同名资源，不会覆盖。

    from wcs.commons.auth import Auth
    from wcs.services.filemanager import BucketManager
    
    # 填写AccessKey和SecretKey
    access_key = ''
    secret_key = ''

    # 生成鉴权对象
    auth = Auth(access_key, secret_key)

    # 设定参数
    srcbucket = ''
    srckey = ''
    dstbucket = ''
    dstkey = ''
    
    # 文件复制
    filemanager = FileManager(auth)
    code, text = filemanager.copy(srcbucket, srckey, dstbucket, dstkey)
 
### 文件移动
该接口提供将指定资源移动为新命名资源。如果目标空间存在同名资源，不会覆盖。

    from wcs.commons.auth import Auth
    from wcs.services.filemanager import BucketManager
    
    # 填写AccessKey和SecretKey
    access_key = ''
    secret_key = ''

    # 生成鉴权对象
    auth = Auth(access_key, secret_key)

    # 设定参数
    srcbucket = ''
    srckey = ''
    dstbucket = ''
    dstkey = ''
    
    # 文件移动
    filemanager = FileManager(auth)
    code, text = filemanager.move(srcbucket, srckey, dstbucket, dstkey)

### 设置文件过期时间

该接口支持用户设置文件的保存期限，超过设置的天数文件自动删除。

**范例：**

    from wcs.commons.auth import Auth
    from wcs.services.filemanager import BucketManager
    
    # 填写AccessKey和SecretKey
    access_key = ''
    secret_key = ''

    # 生成鉴权对象
    auth = Auth(access_key, secret_key)

    # 设定参数
    bucket = ''
    key = ''
    deadline = ''
    
    # 文件移动
    filemanager = FileManager(auth)
    code, text = filemanager.setdeadline(bucket, key, deadline)

## 高级资源管理

### 文件移动
该接口提供将指定资源移动到另一个空间，或者在同一空间重命名。请求参数以如下格式组织，作为请求内容提交，请求参数定义详见[文件移动](https://wcs.chinanetcenter.com/document/API/Fmgr/move)
   
    from wcs.commons.auth import Auth
    from wcs.services.fmgr import Fmgr

    # 填写AccessKey和SecretKey
    access_key = ''
    secret_key = ''

    # 生成鉴权对象
    auth = Auth(access_key, secret_key)

    # 参数配置
    movefops = ''
    notifyurl = ''  //可选
    separate =    //可选

    # 文件移动
    filemanager = Fmgr(auth)
    code, text = filemanager.fmgr_move(movefops, notifyurl=notifyurl, separate=1)

### 文件复制
该接口提供将指定资源复制为新命名资源。请求参数以如下格式组织，作为请求内容提交,请求参数定义详见[文件复制](https://wcs.chinanetcenter.com/document/API/Fmgr/copy)
    
    from wcs.commons.auth import Auth
    from wcs.services.fmgr import Fmgr

    # 填写AccessKey和SecretKey
    access_key = ''
    secret_key = ''

    # 生成鉴权对象
    auth = Auth(access_key, secret_key)

    # 参数配置
    copyfops = ''
    notifyurl = ''  //可选
    separate =    //可选

    # 文件复制
    filemanager = Fmgr(auth)
    code, text = filemanager.fmgr_copy(copyfops, notifyurl=notifyurl, separate=1)

### 文件删除
该接口提供删除指定资源。请求参数以如下格式组织，作为请求内容提交，请求参数定义详见[文件删除](https://wcs.chinanetcenter.com/document/API/Fmgr/delete)
    
    from wcs.commons.auth import Auth
    from wcs.services.fmgr import Fmgr

    # 填写AccessKey和SecretKey
    access_key = ''
    secret_key = ''

    # 生成鉴权对象
    auth = Auth(access_key, secret_key)

    # 参数配置
    delfops = ''
    notifyurl = ''  //可选
    separate =    //可选

    # 文件删除
    filemanager = Fmgr(auth)
    code, text = filemanager.fmgr_delete(delfops, notifyurl=notifyurl, separate=1)

### 文件抓取
该接口提供从指定URL抓取资源，并存储到指定空间。请求参数以如下格式组织，作为请求内容提交，请求参数定义详见[抓取资源](https://wcs.chinanetcenter.com/document/API/Fmgr/fetch)

    from wcs.commons.auth import Auth
    from wcs.services.fmgr import Fmgr

    # 填写AccessKey和SecretKey
    access_key = ''
    secret_key = ''

    # 生成鉴权对象
    auth = Auth(access_key, secret_key)

    # 参数配置
    fetchfops = ''
    notifyurl = ''  //可选
    separate =    //可选

    # 文件抓取
    filemanager = Fmgr(auth)
    code, text = filemanager.fmgr_fetch(fetchfops, notifyurl=notifyurl, separate=1)

### 按前缀删除资源
该接口提供删除符合指定前缀的资源。请求参数以如下格式组织，作为请求内容提交，请求参数详见[前缀删除资源](https://wcs.chinanetcenter.com/document/API/Fmgr/deletePrefix)
    
    from wcs.commons.auth import Auth
    from wcs.services.fmgr import Fmgr

    # 填写AccessKey和SecretKey
    access_key = ''
    secret_key = ''

    # 生成鉴权对象
    auth = Auth(access_key, secret_key)

    # 参数配置
    prefixdelfops = ''
    notifyurl = ''  //可选
    separate =    //可选

    # 按前缀删除
    filemanager = Fmgr(auth)
    code, text = filemanager.prefix_delete(prefixdelfops, notifyurl=notifyurl, separate=1)


### 删除m3u8文件
该接口提供删除指定资源。请求参数以如下格式组织，作为请求内容提交，请求参数详见[删除m3u8文件](https://wcs.chinanetcenter.com/document/API/Fmgr/deletem3u8)
   
    from wcs.commons.auth import Auth
    from wcs.services.fmgr import Fmgr

    # 填写AccessKey和SecretKey
    access_key = ''
    secret_key = ''

    # 生成鉴权对象
    auth = Auth(access_key, secret_key)

    # 参数配置
    prefixdelfops = ''
    notifyurl = ''  //可选
    separate =    //可选

    # m3u8文件删除
    filemanager = Fmgr(auth)
    code, text = filemanager.m3u8_delete(prefixdelfops, notifyurl=notifyurl, separate=1)

### Fmgr任务查询
该接口提供查询Fmgr任务的执行情况。 

注：notifyURL收到的Fmgr任务通知内容的格式与该接口响应内容的格式一致。

    from commons.auth import Auth
    from wcs.services.fmgr import Fmgr
    
    # 填写AccessKey和SecretKey
    access_key = ''
    secret_key = ''

    # 生成鉴权对象
    auth = Auth(access_key, secret_key)
    # 操作persistentId
    persistentId = ''
      
    # 状态查询
    filemanager = Fmgr(auth)
    code,text = filemanager.status(persistentId)

## 持久化操作
以视频截图为例：

    from wcs.commons.auth import Auth
    from wcs.services.persistentfop import PersistentFop
    
    # 要进行的转码操作 
    fops = 'vframe/jpg/offset/10/w/1000/h/1000|saveas/bHVtai10ZXN0OnZmcmFtZS10ZXN0LTEwLmpwZw==' 

    # 填写AccessKey和SecretKey
    access_key = ''
    secret_key = ''

    # 生成鉴权对象
    auth = Auth(access_key, secret_key)   

    # 转码之后保存的文件名
    key = 'vframe.jpg'

    # 操作persistentId
    persistentId = ''
    
    fops = PersistentFop(auth,'<bucket name>')
    # 持久化操作执行
    code,text = fops.execute(fops,key,force=1,notifyurl=notify)
    # 持久化操作状态查询
    code,text = fops.fops_status(persistentId)

## 直播录制文件查询
该接口支持用户查询直播录制的文件列表。请求参数说明如下：

    参数        必填	描述
    channelname	是	直播流名。
    startTime	是	指定直播开始时间。格式为YYYYMMDDmmhhss。
    endTime	    是	指定直播结束时间。格式为YYYYMMDDmmhhss。结束时间不能小于开始时间，且与开始时间间隔不能超过7天。
    bucket	    是	指定空间。
    start	    否	指定起始位置，查询结果从该位置开始返回，如0、1、100 默认值为1，即从查询范围内的第一条记录开始返回。
    limit	    否	指定查询个数。不指定则查询所有记录。


接口调用实例：

    from wcs.commons.auth import Auth 
    from wcs.services.wslive import WsLive

    # 填写AccessKey和SecretKey
    access_key = ''
    secret_key = ''

    # 生成鉴权对象
    auth = Auth(access_key, secret_key) 

    # 参数配置
    channelname = ''
    startTime = ''
    endTime = ''
    bucket = ''
    start = '' //可选
    limit = '' //可选
    
   
    # 直播录制文件查询
    wslive = WsLive(auth)
    code, text = wslive.wslive_list(channelname, startTime, endTime, bucket, start,limit) 

    






    
