#!/usr/bin/python 
#coding=utf-8
#@TIME : 2018/3/5 11:06
#@AUTHOR : CAIYZ
#@FILE : error_deal

CLIENT_ERROR_STATUS = -1
WCS_REQUEST_ID = 'X-Reqid'

class ParameterError(Exception):
    '''
    自定义参数错误异常
    Parameter  error
    '''
    def __init__(self,parameter):
        super(ParameterError,self).__init__()
        self.parameter = parameter

    def __str__(self):
        return self.parameter

class WcsSeriveError(Exception):
    '''
    server error
    '''
    def __init__(self,seriveerror):
        super(WcsSeriveError,self).__init__()
        self.seriveerror = seriveerror

    def __str__(self):
        return self.seriveerror


class WcsError(Exception):
    def __init__(self, status, headers, body, details):
        #: HTTP 状态码
        self.status = status

        #: 请求ID，用于跟踪一个请求。
        self.request_id = headers.get(WCS_REQUEST_ID, '')

        #: HTTP响应体（部分）
        self.body = body

        #: 详细错误信息，是一个string到string的dict
        self.details = details

        #: 错误码
        self.code = self.details.get('Code', '')

        #: 错误信息
        self.message = self.details.get('Message', '')

    def __str__(self):
        error = {'status': self.status,
                 WCS_REQUEST_ID : self.request_id,
                 'details': self.details}
        return str(error)

    def _str_with_body(self):
        error = {'status': self.status,
                 WCS_REQUEST_ID : self.request_id,
                 'details': self.body}
        return str(error)

class ClientError(WcsError):
    def __init__(self, message):
        WcsError.__init__(self,CLIENT_ERROR_STATUS, {}, 'ClientError: ' + message, {})

    def _str_with_body(self):
        error = {'status': self.status,
                 WCS_REQUEST_ID : self.request_id,
                 'details': self.body}
        return str(error)

    def __str__(self):
        return self._str_with_body()

