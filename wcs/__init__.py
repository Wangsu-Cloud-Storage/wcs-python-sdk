__version__ = '2.0.11'

from .commons.auth import Auth
from .commons.compat import urlparse 
from .commons.http import _post,_get
from .commons.util import readfile,file_to_stream,etag

from .services.filemanager import BucketManager
from .services.persistentfop import PersistentFop
from .services.regupload import RegUpload
from .services.sliceupload import SliceUpload
from .services.uploadprogressrecorder import UploadProgressRecorder
