#!/usr/bin/python
## -*- coding: utf-8 -*-
from wcs.commons.config import Config
from wcs.commons.http import _get
from wcs.commons.logme import debug
from wcs.commons.util import https_check
from wcs.services.mgrbase import MgrBase

MGR = Config.mgr_url

class WsLive(MgrBase):
    """直播录制文件查询类
    该类继承自mgrbase
    """
    def __init__(self, auth,url):
        super(WsLive, self).__init__(auth,url)

    def _make_list_url(self, param):
        url = ['{0}/wslive/list'.format(self.mgr_host)] 
        if param:
            url.append(super(WsLive, self)._params_parse(param))
        url = '?'.join(url)
        return url

    def wslive_list(self, channelname, startTime, endTime, bucket, start=None, limit=None):
        query = {
            'channelname' : channelname,
            'startTime' : startTime,
            'endTime' : endTime,
            'bucket' : bucket,
        }
        if start is not None:
            query['start'] = start
        if limit is not None:
            query['limit'] = limit
        url = https_check(self._make_list_url(query))
        if query is not None:
            debug('List params is %s' % query)
        debug('List bucket %s' % bucket)
        return _get(url=url, headers=super(WsLive, self)._gernerate_headers(url)) 
