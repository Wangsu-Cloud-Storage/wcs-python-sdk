# WCS Python SDK用户文档

标签（空格分隔）： 未分类

wcs-python-sdk从v4.0.0版本开始，既可作为Python SDK使用，也可作为命令行工具使用

* SDK的功能包括：文件上传、资源管理、高级资源管理、持久化处理、相应操作状态查询以及直播录制文件查询。
* 命令行工具的功能包括：普通上传、分片上传、资源管理、按前缀删除文件
* 此Python SDK适用于python 2.X

## 安装
推荐使用pip安装

* 直接安装

    >  pip install wcs-python-sdk

## 初始化
在使用SDK之前，您需要获得一对有效的AccessKey和SecretKey签名授权。

可以通过如下方法获得：

1. 开通网宿云存储账号
2. 登录网宿SI平台，在安全管理-秘钥管理查看AccessKey和SecretKey
3. 登录网宿SI平台，在安全管理-域名管理查看上传域名（puturl）和管理域名(mgrurl)。

获取上面4个配置之后，执行如下命令，通过命令行交互的方式对配置信息进行初始化：
wcscmd --configure

更新的配置信息会保存在$HOME目录下的.wcscfg文件中，同时可以通过下面的命令打印上一步添加的配置信息：
wcscmd --dump-config

## wcscmd命令行工具使用(Windows系统执行命令需要添加python再执行,如python wcscmd --help)

#### 查阅工具使用说明
    wcscmd --help
    Commands:
    List objects
    	wcscmd list wcs://BUCKET RESFILE 
    List buckets
    	wcscmd listbucket  
    Download file
    	wcscmd get URL 
    Delete a file
    	wcscmd del wcs://BUCKET/OBJECT 
    Move a file from src bucket to des bucket
    	wcscmd mv wcs://srcBUCKET/srcOBJECT wcs://dstBUCKET/desOBJECT 
    Copy a file from src bucket to des bucket
    	wcscmd cp wcs://srcBUCKET/srcOBJECT wcs://dstBUCKET/desOBJECT 
    Set deadline of file
    	wcscmd setdeadline wcs://BUCKET/OBJECT deadline 
    Get file info
    	wcscmd stat wcs://BUCKET/OBJECT 
    Upload a local file to WCS
    	wcscmd put wcs://BUCKET/OBJECT LOCALFILE 
    Multipart upload a local file to WCS
    	wcscmd multiput wcs://BUCKET/OBJECT LOCALFILE  
    Delete multiple files according to prefix
    	wcscmd deletePrefix wcs://BUCKET PREFIX

#### wcscmd[普通上传](https://wcs.chinanetcenter.com/document/API/FileUpload/Upload)

上传策略可以通过编辑.wcscfg文件中响应的配置项进行定义，也可以通过命令行的option进行临时配置,

     wcscmd put wcs://test/test-1k ./test-1k  --overwrite 1

#### wcscmd[分片上传](https://wcs.chinanetcenter.com/document/API/FileUpload/SliceUpload)
上传策略可以通过编辑.wcscfg文件中响应的配置项进行定义，也可以通过命令行的option进行临时配置，如果需要进行断点续传需要增加--upload-id这个option

     wcscmd multiput wcs://test/test-100M /root/test-100M --upload-id 3IL3ce3kR6kDf4sihxh0LcWUpzTYEKFf
     
#### wcscmd[列举空间列表](https://wcs.chinanetcenter.com/document/API/ResourceManage/listbucket)
    wcscmd listbucket
#### wcscmd[列举空间文件列表](https://wcs.chinanetcenter.com/document/API/ResourceManage/list)
空间test的列举结果会保存在当前目录的result文件中

    wcscmd list wcs://test ./result --limit 4 
    
#### wcscmd下载文件
下载的文件会与源文件同名，并保存在当前目录下
    
    wcscmd get [URL]
    
#### wcscmd[获取文件信息](https://wcs.chinanetcenter.com/document/API/ResourceManage/stat)
    wcscmd stat wcs://test/test-100M
    
#### wcscmd[设置文件保存期限](https://wcs.chinanetcenter.com/document/API/ResourceManage/setdeadline)
保存时间单位为天，0表示尽快删除，-1表示取消过期时间，永久保存

    wcscmd setdeadline wcs://test/test-100M 3
    
#### wcscmd[删除文件](https://wcs.chinanetcenter.com/document/API/ResourceManage/delete)
    wcscmd del wcs://test/test-100M
    
#### wcscmd[按前缀删除文件](https://wcs.chinanetcenter.com/document/API/Fmgr/deletePrefix)

    wcscmd deletePrefix wcs://test test-prefix

#### wcscmd[移动文件](https://wcs.chinanetcenter.com/document/API/ResourceManage/move)
    wcscmd move wcs://srctest/test1 wcs://dsttest/test2
    
#### wcscmd[复制文件](https://wcs.chinanetcenter.com/document/API/ResourceManage/copy)
    wcscmd copy wcs://srctest/test1 wcs://dsttest/test2

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

## Python SDK使用
配置信息初始化
    
    import os
    from os.path import expanduser
    from wcs.commons.config import Config
    from wcs.services.client import Client
    
    config_file = os.path.join(expanduser("~"), ".wcscfg")
    cfg = Config(config_file) #加载配置文件
    cli = Client(cfg) 初始化Client
#### [普通上传](https://wcs.chinanetcenter.com/document/API/FileUpload/Upload)
上传策略通过编辑.wcscfg文件中响应的配置项进行定义

    key = ''
    bucket = ''
    filepath = ''
    cli.simple_upload(filepath, bucket, key)
    
#### [分片上传](https://wcs.chinanetcenter.com/document/API/FileUpload/SliceUpload)
上传策略通过编辑.wcscfg文件中响应的配置项进行定义，断点续传需要提供upload id，可以在上传时传入，或者在.wcscfg中编辑

    key = ''
    bucket = ''
    filepath = ''
    upload_id = ''
    cli.multipart_upload(filepath, bucket, key，upload_id)
    
#### 流地址上传
上传策略通过编辑.wcscfg文件中相应的配置项进行定义，上传时需要提供流地址

    key = ''
    bucket = ''
    stream = ''
    cli.simple_upload(stream, bucket, key)
    
#### [列举空间列表](https://wcs.chinanetcenter.com/document/API/ResourceManage/listbucket)

    cli.list_buckets()

#### [列举空间对象列表](https://wcs.chinanetcenter.com/document/API/ResourceManage/list)
接口相关的4个可选参数（limit，mode，prefix，marker）可以在调用时传入，也可以通过.wcscfg文件中相应的配置项进行定义

    cli.bucket_list(bucket,limit=10)

#### [获取空间存储量](https://wcs.chinanetcenter.com/document/API/ResourceManage/bucketstat)
    startdate = '2017-11-10'
    enddate = '2017-11-12'
    bucket = ''
    cli.bucket_stat(bucket, startdate, enddate)
    
#### [获取文件信息](https://wcs.chinanetcenter.com/document/API/ResourceManage/stat)
    key = ''
    bucket = ''
    cli.stat(bucket, key)
    
#### [文件删除](https://wcs.chinanetcenter.com/document/API/ResourceManage/delete)（同步）
    key = ''
    bucket = ''
    cli.delete(bucket, key)
    
#### [文件移动](https://wcs.chinanetcenter.com/document/API/ResourceManage/move)（同步）
    srcbucket = ''
    srckey = ''
    dstbucket = ''
    dstkey = ''
    cli.move(srcbucket, srckey, dstbucket, dstkey)
#### [文件复制](https://wcs.chinanetcenter.com/document/API/ResourceManage/copy)（同步）
    srcbucket = ''
    srckey = ''
    dstbucket = ''
    dstkey = ''
    cli.copy(srcbucket, srckey, dstbucket, dstkey)
#### [设置文件过期时间](https://wcs.chinanetcenter.com/document/API/ResourceManage/setdeadline)
    bucket = ''
    key = ''
    deadline = 3
    cli.setdeadline(bucket, key, deadline)
#### [文件移动](https://wcs.chinanetcenter.com/document/API/Fmgr/move)（异步）
    srcbucket = 'srcbucket'
    srckey = '1.doc'
    dstbucket = 'dstbucket'
    dstkey = '2.doc'
    resource = urlsafe_base64_encode('%s:%s' % (srcbucket,srckey))
    fops = 'resource/%s/bucket/%s/key/%s' % (resource,urlsafe_base64_encode(dstbucket), urlsafe_base64_encode(dstkey))
    cli.fmgr_move(fops)
#### [文件复制](https://wcs.chinanetcenter.com/document/API/Fmgr/copy)（异步）
    srcbucket = 'srcbucket'
    srckey = '1.doc'
    dstbucket = 'dstbucket'
    dstkey = '2.doc'
    resource = urlsafe_base64_encode('%s:%s' % (srcbucket,srckey))
    fops = 'resource/%s/bucket/%s/key/%s' % (resource,urlsafe_base64_encode(dstbucket), urlsafe_base64_encode(dstkey))
    cli.fmgr_copy(fops)
#### [文件抓取](https://wcs.chinanetcenter.com/document/API/Fmgr/fetch)
    url = 'http://a20170704-weihb.w.wcsapi.biz.matocloud.com/1.doc'
    key = '1.doc'
    bucket = 'test'
    fetchurl = urlsafe_base64_encode(url)
    enbucket = urlsafe_base64_encode(bucket)
    enkey = urlsafe_base64_encode(key)
    fops = 'fetchURL/%s/bucket/%s/key/%s' % (fetchurl, enbucket, enkey)
    cli.fmgr_fetch(fops)
#### 文件删除（异步）
    key = '1.doc'
    bucket = 'test'
    enbucket = urlsafe_base64_encode(bucket)
    enkey = urlsafe_base64_encode(key)
    fops = 'bucket/%s/key/%s' % (enbucket, enkey)
    cli.fmgr_delete(fops)
#### [按前缀删除文件](https://wcs.chinanetcenter.com/document/API/Fmgr/deletePrefix)
    prefix = 'test'
    bucket = 'bucket'
    enbucket = urlsafe_base64_encode(bucket)
    enprefix = urlsafe_base64_encode(prefix)
    fops = 'bucket/%s/prefix/%s' % (enbucket, enprefix)
    cli.prefix_delete(fops)
#### [删除M3U8文件](https://wcs.chinanetcenter.com/document/API/Fmgr/deletem3u8)
    bucket = ''
    key = ''
    enbucket = urlsafe_base64_encode(bucket)
    enkey = urlsafe_base64_encode(key)
    fops = 'bucket/%s/key/%s' % (enbucket, enkey)
    cli.m3u8_delete(fops)
#### 高级资源管理任务查询
    persistentId = ''
    cli.fmgr_status(persistentId)
    
#### [音视频处理](https://wcs.chinanetcenter.com/document/API/Video-op)
    bucket = 'test'
    key = 'test.mp4'
    fops = 'vframe/jpg/offset/1'
    cli.ops_execute(fops,bucket,key)
    
#### 直播录制文件查询
请求参数说明如下：

| 参数       | 必填	| 描述 |
| --------   | -----:   | :----: |
| channelname        | 是      |   直播流名    |
| startTime        | 是      |   指定直播开始时间，格式为YYYYMMDDmmhhss    |
| endTime	        | 是      |   指定直播结束时间，格式为YYYYMMDDmmhhss    |
|bucket             | 是      |指定空间 |
|start              | 否      |指定起始位置，查询结果从该位置开始返回，如0、1、100 默认值为1，即从查询范围内的第一条记录开始返回|
|limit              |否       |指定查询个数。不指定则查询所有记录|




    channelname = ''
    startTime = ''
    endTime = ''
    bucket = ''
    start = '' #可选
    limit = '' #可选
   
    cli.wslive_list(channelname,startTime,startTime, bucket,start,limit)
 



