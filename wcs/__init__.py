__version__ = '1.0.2'

from .commons.auth import Auth
from .commons.compat import urlparse 
from .commons.http import _post,_get
from .commons.util import readfile,file_to_stream,etag

from .services.client import Client
from .services.filemanager import BucketManager
from .services.mgrbase import MgrBase
from .services.persistentfop import PersistentFop
from .services.simpleupload import SimpleUpload
from .services.multipartupload import MultipartUpload
from .services.uploadprogressrecorder import UploadProgressRecorder
from .services.fmgr import Fmgr
from .services.wslive import WsLive
