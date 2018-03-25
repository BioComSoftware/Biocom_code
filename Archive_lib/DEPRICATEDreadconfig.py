#!/usr/bin/python

__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = "BioCom_Commercial_Copyright.py"
__version__     = "0.9.0.0"
__maintainer__  = "Mike Rightmire"
__email__       = "rightmirem@utr.net"
__status__      = "Test"

import re

def readconfig(obj, filename = "config.py"):
    """
    """
    FH = open(filename, "r", 0)
    for line in FH.read().splitlines():
        # Ignore config file comments
        pattern = re.compile('^ *#.*')
        if re.match(pattern, line):continue
        # Check line structure
        if "=" not in line: 
            e = ("Incorrect format in config file line: '" + 
                 str(line) + 
                 "Format is: 'variable = value'" + 
                 "'.\n Please check file: '" + 
                 str(filename) + 
                 "'\n\n")
            raise Exception(e)
        variable, value = line.split("=")
        # remove whitespace from variable only
        pattern = re.compile(r'\s+')
        variable = re.sub(pattern, '', variable)
        obj.__dict__[variable] = value        
    return obj        
    
    