# -*- coding: utf-8 -*-

class PutPolicy(object):
    
    def __init__(self):
       
        self.putpolicy = {}
        self.policy = set(['scope','deadline','saveKey','fsizeLimit','overwrite','returnUrl','returnBody','callbackUrl','callbackBody','persistentNotifyUrl','persistentOps','separate','instant'])

    def set_conf(self, key, value):
        
        if key in self.policy:
            self.putpolicy[key] = value
        else:
            print ("invalid putpolicy param\n")
    
    def get_conf(self, key):
  
        if key in self.policy:
            return key + ":" + self.putpolicy[key]
        else:
            print ("invalid putpolicy param\n")

    def dump_policy(self,cfg):
        if cfg.overwrite:
            self.set_conf('overwrite', int(cfg.overwrite))
        if cfg.returnUrl:
            self.set_conf('returnUrl', str(cfg.returnUrl))
        if cfg.returnBody:
            self.set_conf('returnBody', str(cfg.returnBody))
        if cfg.callbackUrl:
            self.set_conf('callbackUrl', str(cfg.callbackUrl))
        if cfg.callbackBody:
            self.set_conf('callbackBody', str(cfg.callbackBody))
        if cfg.persistentNotifyUrl:
            self.set_conf('persistentNotifyUrl', str(cfg.persistentNotifyUrl))
        if cfg.persistentOps:
            self.set_conf('persistentOps', str(cfg.persistentOps))
        if cfg.contentDetect:
            self.set_conf('contentDetect', str(cfg.contentDetect))
        if cfg.detectNotifyURL:
            self.set_conf('detectNotifyURL', str(cfg.detectNotifyURL))
        if cfg.detectNotifyRule:
            self.set_conf('detectNotifyRule', str(cfg.detectNotifyRule))



        
