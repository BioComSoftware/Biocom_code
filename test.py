#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

class test:
    def __init__(self, l):
        for self.rec in l:
            print (self.rec) 
    
    @property
    def rec(self):
        try:
            return self.REC
        except (AttributeError, ValueError, KeyError) as e:
            raise AttributeError(e)
        
    @rec.setter 
    def rec(self, value):
        if isinstance(value, str):
            self.REC = value
        else:
            err = "Must be a list (value='{V}')".format(V=str(value))
            raise AttributeError(err)
        
    @rec.deleter 
    def rec(self):
        del self.REC
        
if __name__ == '__main__':
    o = test(["A","B",1])         
    