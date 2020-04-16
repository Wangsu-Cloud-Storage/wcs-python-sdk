#!/usr/bin/python 
#coding=utf-8
#@TIME : 2018/3/5 11:06
#@AUTHOR : CAIYZ
#@FILE : error_deal

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

