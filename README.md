# WCS Python SDK使用说明
## [README of English](https://github.com/Wangsu-Cloud-Storage/wcs-python-sdk/blob/master/README-EN.md)
- [概览](#概览)
- [安装](#安装)
- [命令行工具使用](#命令行工具使用)
- [SDK使用](#sdk使用)

## 概览
1. wcs-python-sdk既可作为网宿对象存储SDK使用，也可作为命令行工具使用。
2. 此Python SDK适用于python 2.X，如需python 3.x版本请参考：[wcs-python3-sdk](https://github.com/Wangsu-Cloud-Storage/wcs-python3-sdk)
3. 网宿对象存储API介绍：https://www.wangsu.com/document/644/21558

## 安装
使用pip安装

* 直接安装
```
pip install wcs-python-sdk
```

* 更新方式
```
pip install -U wcs-python-sdk
```

## 命令行工具使用

### 初始化
1、在使用SDK之前，您需要获得一对有效的AccessKey和SecretKey签名授权，可以通过如下方法获得：
* 开通网宿对象存储服务
* 登录 [网宿统一控制台](https://wos.console.wangsu.com) ，在个人中心-用户信息管理-AccessKey管理查看AccessKey和SecretKey
* 登录 [网宿统一控制台](https://wos.console.wangsu.com)，在对象存储空间概览查看上传域名（puturl）和管理域名(mgrurl)。


2、获取所需配置之后，通过命令行交互的方式对配置信息进行初始化：
`wcscmd --configure`

3、更新的配置信息会保存在$HOME目录下的.wcscfg文件中，同时可以通过下面的命令打印上一步添加的配置信息：`wcscmd --dump-config`

.wcscfg文件中的配置参数说明如下：
```
access_key  #用户ak
block_size  #分片上传块大小，默认值4194304，配置时不需要带单位，需要配置为4M的整数倍，默认单位为B
bput_retries  #分片上传，bput请求重传次数
bput_size  #分片上传块内片大小，默认值524288，配置时不需要带单位，片大小不能超过块大小，默认单位为B
callbackBody  #回调上传成功后，服务端提交到callbackurl的数据
callbackUrl  #回调上传成功后，服务端以POST方式请求该地址
concurrency  #分片上传的块并发度，当并发度设置为0时为顺序上传
connection_retries  #请求建立连接时的重传次数，默认3次
connection_timeout  #请求建立连接的超时时间，单位为秒，默认40秒
contentDetect  #文件上传成功后，进行内容鉴定操作
detectNotifyRule  #鉴定结果通知规则设置
detectNotifyURL  #接收鉴定结果的通知地址，要求必须是公网URL地址
force  #强制执行数据处理，默认值为0，不强制执行数据处理并覆盖原结果
ishttps  #是否使用https发起请求，默认False
limit  #列举资源API的limit参数，配置列举条目
marker #列举资源API的maker参数，配置上次列举返回的位置标记，作为本次列举的起点信息
mgr_url  #用户的管理域名
mkblk_retries  #分片上传，mkblk请求重传次数，默认3次
mkfile_retries   #分片上传，mkfile请求重传次数，默认3次
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
upload_id   #非必填，如希望做断点续传，可指定容易识别的唯一字符串标识此次分片上传任务
```


## wcscmd命令行工具使用

注：Windows系统执行命令需要添加python再执行，如`python wcscmd --help`

### 查阅工具使用说明
```
wcscmd --help
Usage: wcscmd [options] COMMAND [parameters]

Wcscmd is a tool for managing objects in WCS Object Storage. It allows for
uploading, downloading and removing objects form buckets

Options:
  -h, --help            show this help message and exit
  --configure           Invoke interactive (re)configuration tool.
  -c FILE, --config=FILE
                        Config file name. Defaults to $HOME/.wcscfg
  --dump-config         Dump current configuration after parsing config file
                        and command line options and exit.
  -s, --ssl             Use https connection when communicating with WCS
  --upload-id=UPLOAD_ID
                        UploadId for Multipart Upload, in case you want
                        continue an existing upload
  --limit=LIMIT         Limit for list objects of bucket
  --prefix=PREFIX       Prefix for list objects of bucket
  --mode=MODE           Mode for list objects of bucket
  --marker=MARKER       Start string for list
  --relevance           Whether modify deadline relevant .ts when modify
                        deadline of m3u8 file
  --debug=DEBUG         Enable debug output.
  --output=OUTPUT       Save request result to specified key,
                        like:<bucket>:<key>
  --notify=NOTIFYURL    Notify url for request result
  --separate=SEPARATE   Whether separate notify, bool type
  --force=FORCE         Whether to enforce data processing, bool type
  --overwrite=OVERWRITE
                        Whether overwrite existed key, bool type
  --returnurl=RETURL    Url for return
  --returnbody=RETBODY  Body of return
  --callbackurl=CBURL   Url for callback
  --callbackbody=CBBODY
                        Body of callback
  --persistentntyurl=PERSISTENTNTYURL
                        Url for persistent ops notify
  --persistentops=PERSISTENTOPS
                        Persistent ops
  --contentdetect=CONTENTDETECT
                        Content detect type
  --detectntyurl=DETECTNTYURL
                        Url for detect notify
  --detectntyrule=DETECTNTYRULE
                        RUle for ectect notify
  --hashalgorithm=HASHALGORITHM
                        Hash algorithm, currently supports 'crc64ecma' for
                        calculating 64-bit CRC value.
  --deadline=DEADLINE   Token expiration time,Unit is second
  --startdate=STARTDATE
                        Start date
  --enddate=ENDDATE     End date
  --islistdetails=ISLISTDETAILS
                        Is list details
  --storagetype=STORAGETYPE
                        storage type
  --traffic_limit=TRAFFIC_LIMIT
                        Upload/Download traffic limit
  --upload_id=UPLOAD_ID
  			UploadId for Multipart Upload, in case you want continue an existing upload
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
	wcscmd fops wcs://BUCKET/OBJECT "fopsparam"   // 避免fopsparam中可能的|导致字符串被切割，可将fopsparam加上双引号
Get fops task results
	wcscmd fopsStatus  persistentId
Get fmgr task results
	wcscmd fmgrStatus  persistentId
```

### wcscmd-普通上传
直接上传，适用于小文件
```
// BUCKET：必填，使用实际空间名称填充，如mybucket
// OBJCET：必填，使用文件存储在对象存储上的实际名称填充，如index.html或html/index.html（文件名使用/可模拟出目录）
// localPath：必填，需要上传文件的本地路径，如/tmp/index.html
wcscmd put wcs://BUCKET/OBJECT localPath
```

### wcscmd-分片上传
分片上传大文件，4M以上的文件即可使用分片上传。
```
// BUCKET：必填，使用实际空间名称填充，如mybucket
// OBJCET：必填，使用文件存储在对象存储上的实际名称填充，如index.html或html/index.html（文件名使用/可模拟出目录）
// localPath：必填，需要上传文件的本地路径，如/tmp/index.html
// --upload-id: 非必填，如希望做断点续传，可指定容易识别的唯一字符串标识此次分片上传任务
wcscmd multiput wcs://BUCKET/OBJECT localPath
```

### wcscmd-列举空间列表
获取空间列表
```
wcscmd listbucket
```

### wcscmd-列举空间文件列表
获取指定空间的文件列表
```
// BUCKET：必填，使用实际空间名称填充，如mybucket
// localPath： 必填，保存文件列表的本地文件路径
// --marker：非必填，使用上一个list请求响应的marker作为此次list的起始位置
wcscmd list wcs://BUCKET localPath --marker <marker>
```

### wcscmd-下载文件
下载文件
```
// URL：必填，由域名+文件名称组成，url需要用''引号包含起来
// fileName： 非必填，文件下载到本地的名称，默认为原文件名
wcscmd get ['URL'] [filename]
```

### wcscmd-获取文件信息
查询文件的基本信息。
```
// BUCKET：必填，使用实际空间名称填充，如mybucket
// OBJCET：必填，使用文件存储在对象存储上的实际名称填充，如index.html
wcscmd stat wcs://BUCKET/OBJECT
```

### wcscmd-设置文件保存期限
设置文件保存期限，到期后自动删除。保存时间单位为天，0表示尽快删除，-1表示取消过期时间，永久保存,要设置-1的时候，需要将整个包含在引号内。
```
// BUCKET：必填，使用实际空间名称填充，如mybucket
// OBJCET：必填，使用文件存储在对象存储上的实际名称填充，如index.html
// day：必填，到期天数，单位天，如30
wcscmd setdeadline wcs://BUCKET/OBJECT <day>
```

### wcscmd-删除文件
删除对象存储上的文件，删除后不可恢复。
```
// BUCKET：必填，使用实际空间名称填充，如mybucket
// OBJCET：必填，使用文件存储在对象存储上的实际名称填充，如index.html
wcscmd del wcs://BUCKET/OBJECT
```

### wcscmd-按前缀删除文件
删除有相同前缀的所有文件，如指定prefix=html/，则会删除html目录下的所有文件。
```
// BUCKET：必填，使用实际空间名称填充，如mybucket
// OBJCET：必填，使用文件存储在对象存储上的实际名称填充，如index.html
// prefix：必填，前缀名称
wcscmd deletePrefix wcs://BUCKET <prefix>
```

### wcscmd-移动文件
在对象存储同空间或者不同空间内移动文件。
```
// SRCBUCKET：必填，源空间名，如mybucket1
// SRCOBJECT：必填，源文件名，如index.html1
// DSTBUCKET：必填，目标空间名，如mybucket2
// DSTOBJECT：必填，目标文件名，如index.html2
wcscmd mv wcs://SRCBUCKET/SRCOBJECT wcs://DSTBUCKET/DSTOBJECT
```

### wcscmd-复制文件
```
// SRCBUCKET：必填，源空间名，如mybucket1
// SRCOBJECT：必填，源文件名，如index.html1
// DSTBUCKET：必填，目标空间名，如mybucket2
// DSTOBJECT：必填，目标文件名，如index.html2
wcscmd cp wcs://SRCBUCKET/SRCOBJECT wcs://DSTBUCKET/DSTOBJECT
```


### 计算文件etag值
wcs-python-sdk提供了计算文件etag值的工具，用户通过命令行的形式体验这个功能
```
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
```
常见问题

1.在相应模块已经安装的情况下，使用工具时出现下面错误：
`pkg_resources.DistributionNotFound: [modulename]`
2.解决方案：
`pip install --upgrade setuptools`

## SDK使用
### 配置信息初始化
```
import os
from os.path import expanduser
from wcs.commons.config import Config
from wcs.services.client import Client

config_file = os.path.join(expanduser("~"), ".wcscfg")
cfg = Config(config_file) #加载配置文件
cli = Client(cfg) 初始化Client  #注：如果要使用多线程同时上传不同文件，请每个线程独立创建client使用，否则不同文件的分片上传信息会重叠
```

SDK通用参数说明
|参数名|参数说明|
|--|--|
|bucket|空间名称，需要在对象存储控制台提前创建|
|key|文件名称，文件存储在对象存储上的完整名称，如index.html、html/index.html等|
|filepath|文件的本地路径|

### 普通上传
普通上传，单次请求上传完整的文件内容。
```
# bucket：必填，使用实际空间名称填充，如mybucket
# key：必填，使用文件存储在对象存储上的实际名称填充，如index.html
# localpath：必填，需要上传文件的本地路径，如/tmp/index.html
# return  (code, body, logid)，如(200, 'aGFzaD1GcXd0WUdReGM4cmoxQ2pycVVMdlY2MFZnZzND', {'x-reqid': '202129121214715120220601111303Aj327Aycsampled'})

cli.simple_upload(filepath, bucket, key)
```

### 分片上传
分片上传，适用于4M以上的大文件。
```
# bucket：必填，使用实际空间名称填充，如mybucket
# key：必填，使用文件存储在对象存储上的实际名称填充，如index.html
# localpath：必填，需要上传文件的本地路径，如/tmp/index.html
# upload_id：非必填，如希望做断点续传，可指定容易识别的唯一字符串标识此次分片上传任务
# return  (code, body, logid)，如(200, {'key': '100-2M', 'hash': 'lkD-baE6ugMtIAGaarh7j6ToUg7h'}, {'x-reqid': '202129121214715120220601111741hVVCYXwFsampled'})

cli.multipart_upload(filepath, bucket, key，<upload_id>)  
```
另外，当前上传记录的格式是在tmp\_record\_folder目录下，生成已当前上传任务的upload id命名的目录，然后在目录tmp\_record\_folder/upload id下生成多个文件，每个文件以块offset命名，并记录了这个块的上传结果

### 高级上传
该接口用于自动选择是普通上传还是分片上传，默认的multi_size 为20M （入参单位为M），小于等于20M 使用普通上传，大于20M使用分片上传
```
# bucket：必填，使用实际空间名称填充，如mybucket
# key：必填，使用文件存储在对象存储上的实际名称填充，如index.html
# localpath：必填，需要上传文件的本地路径，如/tmp/index.html
# upload_id：非必填，如希望做断点续传，可指定容易识别的唯一字符串标识此次分片上传任务

cli.smart_upload(filepath, bucket, key, <upload_id>, multi_size=20)
```
另外，当前上传记录的格式是在tmp\_record\_folder目录下，生成已当前上传任务的upload id命名的目录，然后在目录tmp\_record\_folder/upload id下生成多个文件，每个文件以块offset命名，并记录了这个块的上传结果

### 流地址上传
上传文件流
```
# bucket：必填，使用实际空间名称填充，如mybucket
# key：必填，使用文件存储在对象存储上的实际名称填充，如index.html
# stream：必填，文件流信息
cli.stream_upload(stream, bucket, key)
```

### 列举空间列表
```
cli.list_buckets()
```

### 列举空间对象列表
接口相关的4个可选参数（limit，mode，prefix，marker）可以在调用时传入，也可以通过.wcscfg文件中相应的配置项进行定义
```
# bucket 必填，空间名称
# limit 非必填，指定单次列举返回的文件数，最大支持1000条
# prefix 非必填，列举指定前缀的文件列表
cli.bucket_list(bucket,limit=1000,prefix="html/")
说明：prefix 参数传入不需要base64安全编码
```

### 获取空间存储量
统计指定时间范围内空间的存储量
```
# startdate 必填，统计开始时间，如'2021-11-10'
# enddate 必填，统计结束时间，如'2021-11-12'
# bucket 必填，空间名称
cli.bucket_stat(bucket, startdate, enddate)
```

### 获取文件信息
查看文件的基础信息
```
# bucket 必填，空间名称
# key 必填，文件名称
cli.stat(bucket, key)
```

### 文件删除
删除文件，删除后不可恢复
```
# bucket 必填，空间名称
# key 必填，文件名称
cli.delete(bucket, key)
```

### 文件移动
在相同空间内或者不同空间之间移动文件
```
# srcbucket 必填，源空间名称
# srckey 必填，源文件名称
# dstbucket 必填，目标空间名称
# dstkey 必填，目标文件名称
cli.move(srcbucket, srckey, dstbucket, dstkey)
```

### 文件复制
在相同空间内或者不同空间之间复制文件
```
# srcbucket 必填，源空间名称
# srckey 必填，源文件名称
# dstbucket 必填，目标空间名称
# dstkey 必填，目标文件名称
cli.copy(srcbucket, srckey, dstbucket, dstkey)
```

### 设置文件过期时间
设置文件保存期限，到期后自动删除。保存时间单位为天，0表示尽快删除，-1表示取消过期时间，永久保存,要设置-1的时候，需要将整个包含在引号内。
```
# bucket 必填，使用实际空间名称填充，如mybucket
# key 必填，使用文件存储在对象存储上的实际名称填充，如index.html
# deadline 必填，到期天数，单位天，如30，则文件会在当天日期的30天后被过期删除
cli.setdeadline(bucket, key, deadline)
```

### 文件移动
使用异步任务的方式，移动文件，支持一个请求添加多个移动任务
```
srcbucket = 'srcbucket'  //源空间名称
srckey = '1.doc'        //源文件名称
dstbucket = 'dstbucket'   //目标空间名称
dstkey = '2.doc'          //目标文件名称
resource = urlsafe_base64_encode('%s:%s' % (srcbucket,srckey))
fops = 'resource/%s/bucket/%s/key/%s' % (resource,urlsafe_base64_encode(dstbucket), urlsafe_base64_encode(dstkey))
cli.fmgr_move(fops)
```

### 文件复制
使用异步任务的方式，复制文件，支持一个请求添加多个复制任务
```
srcbucket = 'srcbucket'  //源空间名称
srckey = '1.doc'        //源文件名称
dstbucket = 'dstbucket'   //目标空间名称
dstkey = '2.doc'          //目标文件名称
resource = urlsafe_base64_encode('%s:%s' % (srcbucket,srckey))
fops = 'resource/%s/bucket/%s/key/%s' % (resource,urlsafe_base64_encode(dstbucket), urlsafe_base64_encode(dstkey))
cli.fmgr_copy(fops)
```

### 文件抓取
使用异步任务的方式，将指定的资源（URL）的文件抓取到对象存储空间内。
```
url = 'http://a20170704-weihb.w.wcsapi.biz.matocloud.com/1.doc'  //需要抓取的文件地址（需要支持公网访问）
key = '1.doc'       // 存储在对象存储空间上的文件名称
bucket = 'test'     // 空间名称
fetchurl = urlsafe_base64_encode(url)
enbucket = urlsafe_base64_encode(bucket)
enkey = urlsafe_base64_encode(key)
fops = 'fetchURL/%s/bucket/%s/key/%s' % (fetchurl, enbucket, enkey)
cli.fmgr_fetch(fops)
```

### 文件删除（异步）
使用异步任务的方式，删除文件，支持一个请求添加多个删除任务
```
key = '1.doc'
bucket = 'test'
enbucket = urlsafe_base64_encode(bucket)
enkey = urlsafe_base64_encode(key)
fops = 'bucket/%s/key/%s' % (enbucket, enkey)
cli.fmgr_delete(fops)
```

### 按前缀删除文件
删除有相同前缀的所有文件，如指定prefix=html/，则会删除html目录下的所有文件。
```
prefix = 'test/'   //需要删除的文件共同前缀，如prefix=test/，则会删除根路径下test目录下的所有文件
bucket = 'bucket'   // 空间名称
enbucket = urlsafe_base64_encode(bucket)
enprefix = urlsafe_base64_encode(prefix)
fops = 'bucket/%s/prefix/%s' % (enbucket, enprefix)
cli.prefix_delete(fops)
```

### 删除M3U8文件
删除m3u8文件以及关联的ts文件
```
bucket = ''     // 空间名称
key = ''        // m3u8文件名称
enbucket = urlsafe_base64_encode(bucket)
enkey = urlsafe_base64_encode(key)
fops = 'bucket/%s/key/%s' % (enbucket, enkey)
cli.m3u8_delete(fops)
```

### 高级资源管理任务查询
查询异步删除、复制等任务的状态
```
persistentId = ''  // 下发异步任务时响应的任务ID
cli.fmgr_status(persistentId)
```

### 音视频处理
```
bucket = 'test'     // 空间名称
key = 'test.mp4'    // 文件名称
fops = 'vframe/jpg/offset/1'   // 转码指令
cli.ops_execute(fops,bucket,key)
```

## 计算文件crc64的三种方式
### 方式1：
wcscmd[计算文件的crc64值]
```wcscmd crc64 ./test-1k```

### 方式2：
计算整个文件的crc64值，入参为[file,is_path=True],传入为文件流时候，需配置参数is_path=False
```
from wcs.commons.util import file_crc64
filepath = 'xxxx'#文件路径
crc64Value = file_crc64(filepath)

from wcs.commons.util import file_crc64
fileStream = 'xxxx' #文件流
crc64Value = file_crc64(fileStream,is_path=False)

计算文件文件流的crc64值，入参为文件流，文件流过大时候，不建议用该方式。建议使用file_crc64，入参为isPath=False的方式
from wcs.commons.util import crc64
crc64Value = crc64(stream)
```

### 方式3：
wcs-python-sdk提供了计算文件crc64值的工具，用户通过命令行的形式体验这个功能
```
usage: WCS Python SDK [-h] {crc64} ...
positional arguments:
    {crc64}
    crc64     crc64 [file...]
optional arguments:
    -h, --help  show this help message and exit

/usr/bin/wcs_crc64_cal crc64 filepath1 filepath2
[filepath1, filepath2]
1798452899179748974 5299837023984967047
```
