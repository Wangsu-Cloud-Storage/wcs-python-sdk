# WCS Python SDK用户文档

wcs-python-sdk从v4.0.0版本开始，既可作为Python SDK使用，也可作为命令行工具使用

* SDK的功能包括：文件上传、资源管理、高级资源管理、持久化处理、相应操作状态查询以及直播录制文件查询。
* 命令行工具的功能包括：普通上传、分片上传、资源管理、按前缀删除文件
* 此Python SDK适用于python 2.X

## 安装
推荐使用pip安装

* 直接安装

    >  pip install wcs-python-sdk

* 更新方式
   >pip install -U wcs-python-sdk

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

.wcscfg文件中的配置参数说明如下：

    access_key  #用户ak
    block_size  #分片上传块大小，默认值4194304，配置时不需要带单位，默认单位为B
    bput_retries  #分片上传，bput请求重传次数
    bput_size  #分片上传块内片大小，默认值524288，配置时不需要带单位，默认单位为B
    callbackBody  #回调上传成功后，服务端提交到callbackurl的数据
    callbackUrl  #回调上传成功后，服务端以POST方式请求该地址
    concurrency  #分片上传的块并发度，当并发度设置为0时为顺序上传
    connection_retries  #请求建立连接时的重传次数
    connection_timeout  #请求建立连接的超时时间
    contentDetect  #文件上传成功后，进行内容鉴定操作
    detectNotifyRule  #鉴定结果通知规则设置
    detectNotifyURL  #接收鉴定结果的通知地址，要求必须是公网URL地址
    force  #强制执行数据处理，默认值为0，不强制执行数据处理并覆盖原结果
    ishttps  #是否使用https发起请求
    limit  #列举资源API的limit参数，配置列举条目
    marker #列举资源API的maker参数，配置上次列举返回的位置标记，作为本次列举的起点信息
    mgr_url  #用户的管理域名
    mkblk_retries  #分片上传，mkblk请求重传次数
    mkfile_retries   #分片上传，mkfile请求重传次数
    mode   #列举资源API的mode参数，配置列表排序方式
    notifyurl  #异步处理API处理结果通知接收URL
    output   #将任务处理结果的描述信息保存到指定文件，格式为：<bucket>:<key>。
    overwrite   #上传API发现文件已存在时是否覆盖
    persistentNotifyUrl   #接收预处理结果通知的地址
    persistentOps  #文件上传成功后，预处理指令列表
    prefix  #列举资源API的prefix参数
    put_url   #用户上传域名
    returnBody  #上传成功后，自定义最终返回給上传端的数据
    returnUrl  #上传成功后，服务端以POST方式请求该地址
    secret_key  #用户sk
    separate  #处理指令是否分开通知
    tmp_record_folder  #分片上传上传进度记录目录
    upload_id   #分片上传断点续传的任务id


## wcscmd命令行工具使用

Windows系统执行命令需要添加python再执行,如python wcscmd --help

#### 查阅工具使用说明
    wcscmd --help
    Commands:
    List objects  支持后面加参数 如--prefix aa
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
    Fops audio/video processing
    	wcscmd fops wcs://BUCKET/OBJECT fopsparm
    Get fops task results
    	wcscmd fopsStatus  persistentId
    Get fmgr task results
    	wcscmd fmgrStatus  persistentId

#### wcscmd[普通上传](https://wcs.chinanetcenter.com/document/API/FileUpload/Upload)

上传策略可以通过编辑.wcscfg文件中响应的配置项进行定义，也可以通过命令行的option进行临时配置,

     wcscmd put wcs://test/test-1k ./test-1k  --overwrite 1

#### wcscmd[分片上传](https://wcs.chinanetcenter.com/document/API/FileUpload/SliceUpload)
上传策略可以通过编辑.wcscfg文件中响应的配置项进行定义，也可以通过命令行的option进行临时配置，如果需要进行断点续传需要增加--upload-id这个option，这个upload-id的优先级高于在.wcscfg中配置的upload id

     wcscmd multiput wcs://test/test-100M /root/test-100M --upload-id 3IL3ce3kR6kDf4sihxh0LcWUpzTYEKFf
     
#### wcscmd[列举空间列表](https://wcs.chinanetcenter.com/document/API/ResourceManage/listbucket)
    wcscmd listbucket

#### wcscmd[列举空间文件列表](https://wcs.chinanetcenter.com/document/API/ResourceManage/list)
空间test的列举结果会保存在当前目录的result文件中

    wcscmd list wcs://test ./result --limit 4  --marker 2
    
#### wcscmd下载文件
未带filename 参数，下载的文件默认会与源文件同名，并保存在当前目录下
带有filename 参数，下载文件保存在当前目录下，文件名称为参数filename
url 需要用''引号包含起来
    
    wcscmd get [URL] [filename]
    
#### wcscmd[获取文件信息](https://wcs.chinanetcenter.com/document/API/ResourceManage/stat)
    wcscmd stat wcs://test/test-100M
    
#### wcscmd[设置文件保存期限](https://wcs.chinanetcenter.com/document/API/ResourceManage/setdeadline)
保存时间单位为天，0表示尽快删除，-1表示取消过期时间，永久保存,要设置-1的时候，需要将整个包含在引号内

    wcscmd setdeadline wcs://test/test-100M 3
    wcscmd setdeadline wcs://test/test-100M '"-1"'

    
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
上传策略通过编辑.wcscfg文件中响应的配置项进行定义，断点续传需要提供upload id，在上传时传入，这个upload id优先级高于在.wcscfg中配置的upload id

    key = ''
    bucket = ''
    filepath = ''
    upload_id = ''
    cli.multipart_upload(filepath, bucket, key，upload_id)

另外，当前上传记录的格式是在tmp\_record\_folder目录下，生成已当前上传任务的upload id命名的目录，然后在目录tmp\_record\_folder/upload id下生成多个文件，每个文件以块offset命名，并记录了这个块的上传结果
    
#### 流地址上传
上传策略通过编辑.wcscfg文件中相应的配置项进行定义，上传时需要提供流地址

    key = ''
    bucket = ''
    stream = ''
    cli.simple_upload(stream, bucket, key)
    
#### [列举空间列表](https://wcs.chinanetcenter.com/document/API/ResourceManage/listbucket)

    cli.list_buckets()
    说明：prefix 参数传入不需要base64安全编码

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
 



