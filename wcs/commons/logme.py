import os
import logging
import errno
import time


#if os.path.exists(path) is False:
#    try:
#        os.mkdir(path)
#    except OSError as exc:
#        raise exc

logger = logging.getLogger("wcs_python_sdk")
time_obj = time.gmtime()
log_time = "{year}_{month}_{day}".format(year=time_obj.tm_year,month=time_obj.tm_mon,day=time_obj.tm_mday)

def debug(msg):
    logger.setLevel(logging.DEBUG)
    debughandler = logging.StreamHandler()
    debughandler.setLevel(logging.DEBUG)
    fmt = '%(asctime)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    debughandler.setFormatter(formatter)
    logger.addHandler(debughandler)
    logger.debug(msg)
    logger.removeHandler(debughandler)

#def warning(msg):
#    logger.setLevel(logging.WARNING)
#    logfile = os.path.join(path, "warnging_%s.log" % log_time)
#    warnhandler = logging.FileHandler(logfile)
#    warnhandler.setLevel(logging.WARNING)
#    fmt = '%(asctime)s - %(levelname)s - %(message)s' 
#    formatter = logging.Formatter(fmt)
#    warnhandler.setFormatter(formatter)
#    logger.addHandler(warnhandler)
#    logger.warning(msg)
#    logger.removeHandler(warnhandler)

def error(msg):
    logger.setLevel(logging.ERROR)
    errorhandler = logging.StreamHandler()
    errorhandler.setLevel(logging.ERROR)
    fmt = '%(asctime)s - %(levelname)s - %(message)s' 
    formatter = logging.Formatter(fmt)
    errorhandler.setFormatter(formatter)
    logger.addHandler(errorhandler)
    logger.error(msg)
    logger.removeHandler(errorhandler)

        

