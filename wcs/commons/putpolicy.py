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

