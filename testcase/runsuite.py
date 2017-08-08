import unittest 
from testcase.testcases import BucketManagerTestCase
from testcase.testcases import FmgrTestCase
from testcase.testcases import AuthTestCase
from testcase.testcases import RegUploadTestCase
from testcase.testcases import SliceUploadTestCase
from testcase.testcases import BucketManagerTestCase
from testcase.testcases import PerFopTestCase
from testcase.testcases import WsLiveTestCase


if  __name__ == '__main__':
    suite = unittest.TestSuite()
    
    # add testcases in BucketManager
    suite.addTest(BucketManagerTestCase("test_list"))
    suite.addTest(BucketManagerTestCase("test_stat"))
    suite.addTest(BucketManagerTestCase("test_delete"))
    suite.addTest(BucketManagerTestCase("test_copy"))
    suite.addTest(BucketManagerTestCase("test_move"))
    suite.addTest(BucketManagerTestCase("test_setDL"))

    # add testcases in Fmgr
    suite.addTest(FmgrTestCase("test_copy"))
    suite.addTest(FmgrTestCase("test_move"))
    suite.addTest(FmgrTestCase("test_fetch"))
    suite.addTest(FmgrTestCase("test_delete"))
    suite.addTest(FmgrTestCase("test_pre_delete"))
    suite.addTest(FmgrTestCase("test_m3u8_delete"))

    # add testcases in Auth
    suite.addTest(AuthTestCase("test_upload_token"))
    suite.addTest(AuthTestCase("test_manager_token"))

    # add testcases in RegUpload
    suite.addTest(RegUploadTestCase("test_regupload"))
    suite.addTest(RegUploadTestCase("test_callback"))
    suite.addTest(RegUploadTestCase("test_notify"))
 
    # add testcases in SliceUpload
    suite.addTest(SliceUploadTestCase("test_upload"))

    # add testcases in PerFop
    suite.addTest(PerFopTestCase("test_fops"))
  
    # add testcases in WsLive
    #suite.addTest(WsLiveTestCase("test_wslivelist"))
    
    runner = unittest.TextTestRunner()
    runner.run(suite)
