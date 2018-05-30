##############################################################################
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU LGPL License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# See the files gpl.txt and lgpl.txt packaged with this file.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = "LGPLv3"
__license_file__= "lgpl.txt"
__version__     = "0.9.10.0"
__maintainer__  = "Mike Rightmire"
__email__       = "Mike.Rightmire@BiocomSoftware.com"
__status__      = "Development"

##############################################################################
#         USAGE = "{C}.{M}: Value must be a string containing a full path to a temporary file or directory. ".format(C = self.__class__.__name__, M = inspect.stack()[0][3])

from BiocomCommon.checks import Checks
checks = Checks()
_slash = checks.directory_delimiter() 
from BiocomCommon.loghandler import log
from BiocomCommon.errorhandler.customexceptions import PropertyNotValidValueError, PropertyNotSetError, PropertyCannotBeSetError
from inspect import stack

import atexit
import ntpath
import os
import re
import tempfile

class BlankParameter(Exception):
    def __init__(self, message, *args, **kwargs):
        log.error("Attribute.setter '{M}' called with empty string. This may be a part of normal operation. ".format(M = message))
        super(BlankParameter, self).__init__(message, *args, **kwargs)
        

class TMP(object):
    """
    """
    def __init__(self, path = None, delete = False, *args, **kwargs):
        USAGE = "{C}.{M}: 'path' must be a string containing a full path to a temp file, a temp directory, or the keyword 'file' or 'directory' in order to create them generically.".format(C = self.__class__.__name__, M = stack()[0][3])
        self.path = path # Just for reference of original parameter
        self.delete = delete
        _path = str(path)
        # The default (no indicator) is to create a temp directory only
        # A automatically named temp file can be created on the fly by accessing
        # the self.file
        if path is None or path == '' or re.match("^dir?e?c?t?o?r?y?$", _path, re.IGNORECASE):
            log.debug("Creating a tempfile.mkdtemp object") 
            self.directory = 'mkdtemp'
        elif _path.endswith(_slash): 
            log.debug("Creating a temporary directory '{P}'".format(P = _path)) 
            self.directory = _path
        elif re.match("^fi?l?e?$", _path, re.IGNORECASE) or re.match("^namedtemporaryfile$", _path, re.IGNORECASE):
            log.debug("Creating a tempfile.NamedTemporaryFile object") 
            self.file = 'NamedTemporaryFile'
        elif re.match("^mkstemp$", _path, re.IGNORECASE):
            raise NotImplementedError()
        elif _path.startswith(_slash) and not _path.endswith(_slash):
            log.debug("Creating a temporary file '{P}'".format(P = _path)) 
            self.file = _path
        else:
            raise PropertyNotValidValueError(stack()[0][3], value = path, USAGE = USAGE) 

        atexit.register(self._cleanup)
        
    def _cleanup(self):
        log.debug("Closing file handler '{FH}'".format(FH = self.file_handler))
        self.file_handler.close()
        if self.delete:
            try:
                log.debug("Deleting directory '{D}'".format(D = self.directory))
                os.remove(self.directory)
            except Exception as e:
                log.warning("Unable to remove directory '{D}' ({E})".format(D = self.directory, E = str(e)))
    
    @property
    def delete(self):
        try:
            return self.DELETE
        except (AttributeError, NameError, KeyError) as e:
            return False
        
    @delete.setter
    def delete(self, value):
        if value: self.DELETE = True
        else:self.DELETE = False

    @delete.deleter
    def delete(self):
        del self.DELETE
        
    @property
    def directory(self):
        return self.DIRECTORY
    
    @directory.setter
    def directory(self, value):
        def _mkdir(_directory):
            if not _directory.endswith(_slash): _directory += _slash
            if checks.pathExists(_directory):
               if checks.isDir(_directory): 
                   self.DIRECTORY = _directory
                   self.TEMPFILE_OBJECT = None
                   return
               
               else:
                   err = "Path '{V}' exists but is not a directory. ".format(V = str(value))
                   raise ValueError(err)
            
            else: # Does NOT exist
               try: 
                   os.mkdir(_directory)
                   self.DIRECTORY = _directory
                   return
               except OSError as e:
                   err = "Unable to make temporary directory path '{V}' ({E})".format(V = str(value), E = str(e))
                   raise OSError(err)
            
        USAGE = "The 'directory' attribute must be a full path ending in a directory marker (slash) to an existing directory or a new directory to be created. I.e. '/dir1/dir2/'."
        value = str(value)
        if value == 'mkdtemp':
            self.TEMPFILE_OBJECT = tempfile.mkdtemp('.tmpdir')
            self.DIRECTORY = self.TEMPFILE_OBJECT + _slash
            return 
        
        if ntpath.isabs(value):
                _mkdir(value)
        else:
            raise PropertyNotValidValueError(stack()[0][3], value = value, USAGE = USAGE) 

    @directory.deleter
    def directory(self):
        del self.DIRECTORY

    @property
    def file(self):
        try:
            return self.FILE
        # If self.FILE does nto exist, create temptfile
        except (AttributeError, NameError, KeyError) as e:
            # This means a temporary directory was instantiated, but
            # they want a new temporary file, so create a file in the directory
            # <__main__.test object at 0x100e8ce50>
            self.file = "CreateTemporaryFile"
        return self.FILE

    @file.setter
    def file(self, value):
        def _open(_file):
            fullpath = self.directory + _file            
            
            try:
                self.TEMPFILE_OBJECT = None
                self.file_handler = open(fullpath, 'a+', 0)
                self.FILE = _file
                return True
            
            except IOError as e:
                err = "Unable to open the file '{F} ({E}).'".format(F = self.FILE, E = e.message)
                raise type(e)(err)
            
        USAGE = ''
        if value == 'NamedTemporaryFile':
            self.file_handler = self.TEMPFILE_OBJECT = tempfile.NamedTemporaryFile(suffix = '.tmp', delete = False)
            self.DIRECTORY = ntpath.dirname(self.TEMPFILE_OBJECT.name) + _slash
            self.FILE  = ntpath.basename(self.TEMPFILE_OBJECT.name) 
            return
        
        elif value == 'CreateTemporaryFile':
            match = re.match("^(.*0x)(.*)(\>)", str(self))
            if match:
                _open(match.groups()[1] + '.tmp')
            else:
                err = "Unable to create filename from 'str(self)'. re did not match. "
                raise RuntimeError(err)
            
        elif value.startswith(_slash):
            if value.endswith(_slash):
                # Actually a directory
                self.directory = value
                return 
            else: # NOT ends with slash, but starts with slash
                self.directory = ntpath.dirname(value)
                _filename = ntpath.basename(value)
                _open(_filename)
                return 
        else: # Does not start with slash
            #Assumes a filename and goes with it. +
            _open(value)
            return
        
    @file.deleter
    def file(self):
        raise NotImplementedError()

    @property
    def file_handler(self):
        try:
            return self.FILE_HANDLER 
        except (AttributeError, NameError, KeyError) as e:
            self.file = "CreateTemporaryFile"
            return self.FILE_HANDLER
        
    @file_handler.setter
    def file_handler(self, value):
        if re.match("^\<open file.*\>", str(value)):
            self.FILE_HANDLER = value
        else:
            raise PropertyNotValidValueError(stack()[0][3], value = value)

    @file_handler.deleter
    def file_handler(self):
        del self.FILE_HANDLER 

    @property
    def name(self):
        """
        This exists only for backwards compatibility with Python tempfile objects
        """
        try:
            # If a temp file, then this is set
            return self.FILE 
        except (AttributeError, NameError, KeyError) as e:
            #if no self.FILE, then directory
            return self.directory 
    
    @name.setter
    def name(self, value):
        raise PropertyCannotBeSetError(stack()[0][3], value = value)        
        
    @name.deleter
    def name(self):
        raise NotImplementedError()

# Public methods        
    def seek(self, location):
        self.file_handler.seek(location)
        return True

    def write(self, value):
        """
        Writes to the end of the temp file. 
        NOTE: New lines MUST be included int he text
        """
        self.file_handler.read() # Takes us to end of file
        self.file_handler.write(value) # Write to EOF
        return True

    def writeline(self, value):
        self.write(value + "\n")

    def writeln(self, value):
        self.writeline(value)
            
    def writelines(self, value):
        for line in value:
            self.writeline(line)
            
    def read(self):
        # All as single string
            self.file_handler.seek(0)
            return self.file_handler.read()

    def readline(self):
        for line in self.read():
            yield line
      
    def readlines(self):
        # All as list
            result = []
            for line in self.read():
                result.append(line)
            return result
        
    def close():
        self._cleanup()
    
if __name__ == '__main__':
    log.debug("Starting main...", logfile = 'syslog', log_level = 10, screendump = True)
    o = TMP()
    print "o = ", o
    print "o.directory =", o.directory
    print "o.file =", o.file
    
#     o = TMP('/Users/mikes/Documents/tmp/testfile')
#     o = TMP('/Users/mikes/Documents/tmp/')
#     o = TMP('file')
#     o = TMP('dir')
    
    #===========================================================================
    # print "tempfile_object=", o.TEMPFILE_OBJECT
    # print "name=", o.name
    # print "directory=", o.directory
    # print "path=", o.path
    # print 'o.name=', o.name
    # try:
    #     print 'FILE_HANDLER =', o.FILE_HANDLER
    # except:
    #     print 'FILE_HANDLER does not yet exist'
    # print "o.file =", o.file
    # print 'o.seek(0)', o.seek(0)
    # #===========================================================================
    # # print "WRITE----------------------------"
    # # for i in "0123456789": o.write(i)    
    # # print 'read-------------'
    # # print o.read()
    # # print 'readline-------------'
    # # for i in o.readline(): print i
    # # print 'readlines---------------'
    # # print o.readlines()
    # # print 'o.file = ', o.file
    # #===========================================================================
    # print "WRITEline----------------------------"
    # for i in "0123456789": o.writeline(i)    
    # print 'read-------------'
    # print o.read()
    # print 'readline-------------'
    # for i in o.readline(): print i
    # print 'readlines---------------'
    # print o.readlines()
    # print 'o.file = ', o.file
    #===========================================================================
