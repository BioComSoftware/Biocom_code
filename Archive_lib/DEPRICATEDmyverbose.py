#!/usr/bin/python

__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = "BioCom_GPL_Copyright.py"
__version__     = "0.9.0.0"
__maintainer__  = "Mike Rightmire"
__email__       = "rightmirem@utr.net"
__status__      = "Test"

import os
import re 
import sys

#from general import *
from time import strftime

# Avoiding "logging" module because it is cumbersome for this script's goals

            
class Verbose(object):
    """
    myverbose.Verbose(<max_verbose_level>, [[stdout], [file1], [file2]])
    
    User methods:
     obj.out = passes message and verbosity level to all file handles 
     obj.log  = passes messages verbosity level ONLY to LOGFILE(s)
     obj.screen = passes messages and verbosity level only to screen

    PSEUDO-DECORATORS
    You can simplify the verbose.out calls with the following almost decorators:
    vobject = myverbose.Verbose(10, [file])
    vout = vobject.vout()
    vout(10, "message")
    # instead of vobject.out(10, "message") 
    
    Also vlog = vobject.vlog()
    and  vprint = vobject.vprint()
     global variable "error_messages" holds a list of errors which may have
      occurred during module run. I.e.
      for message in obj.error_messages:
          print message
    
    Creates an object used to pass verbose messages to screen 
    and/or multiple files. Intended to be used within scripts. Use with 
    agparse or similar. max_level can be any integer (don't go crazy) and 
    can output to any number of files. I.e. python script.py -vv
              
    parser = argparse.ArgumentParser(usage=USAGE)
    parser.add_argument('-v', action='store',dest='max_level', default='1')
    parser.add_argument('-vv', action='store',dest='max_level', default='2')
    # -vv mean max_level = 2
    options = parser.parse_args()
    verbose = output.Verbose(max_level, 
                            "stdout", 
                            "/path/path/filename-1",
                            "/path/path/filename-2", 
                            "/path/path/filename-n")
                            
    'verbose' will dump to stdout, and all three files. If object 
      called with a higher verbose number than what it was created with, 
      message is not output. I.e.
      
    'verbose' object was created with max_level = 2  
    verbose.out(1, "Prints verbose output level 1 or equiv of '-v' ")
    verbose.out(2, "Prints verbose output level 2 or equiv of '-vv' ")
    verbose.out(3, "Will not output, because object created with max level 2")
    
    if verbose object created with max_level '0', output suppressed 
    completely. I.e.    
    
    verbose = output.Verbose(0, "stdout", "/path/filename")
    verbose.out(1, "Nothing printed when verbose object called") 
    
    NOTE: Remember, when working on a windows system, precurse the logfile
     path with "r", as in (r"c:\windows\Users\myuser\logfile.out")
             
     !! Known issue. For an unknown reason the file handles get closed, 
     initiating the logging BUG: http://bugs.python.org/issue6333 
     and gives you an (apparently) uncatchable ValueError...and
     chokes the script. NOTE TO SELF: Figure out why the files are 
     closing, and stop either it or figure out the BUGFIX workaround :-)
     
     RECCOMENDATIONS:
     Verbosity of...
      0   = NO output
      10  = Regular informational messages
      30  = Basic troubleshooting messages (v)
      100 = Extremely detailed troubleshooting messages (vvv)

    """
    def __init__(self, verbosity=0, *args):
        """
        """
        self.date = False
        self.screen_pattern = ("^.*std.*out.*$|" + 
                               "^.*screen.*$|" + 
                               "^.*pri.*$|" + 
                               "^.*def.*$|" + 
                               "^.*moni.*$")
        self.verbosity = int(verbosity)
        self._convert_args_to_list(args)
        for item in self.args:
            if re.match('.*date.*', str(item).lower()):
                self.date = True
                self.args.remove(item)
        self.FH_error_messages = []
        self._open_files()    

    def _add_FH(self, path):
        try:
            self.FH.append(open(path, "a", 0))
        except IOError, e:
            _error = "Unable to open file. "
            _error = _error + "IOError: " + str(e)
            if "errno 22" in str(e).lower():
                _error = _error + "If this is a windows system, "
                _error = ( _error + 
                           "verify an 'r' is placed " + 
                           "in front of file path.")
            if "errno 13" in str(e).lower():
                _error = _error + "Verify file is not 'read only' "
                _error = _error + "and that you have permissions."
            self.FH_error_messages.append(_error)

    def _add_datestamp(self, message):
        """
        """
        if self.date:
            message = str(message)
            datestamp = "%s %s " % (strftime("%d-%m-%Y"), strftime("%H:%M:%S"))
            message = str(datestamp) + message
        return message

    def _convert_args_to_list(self, args):
        self.args = []
        if args == ():
            self.args = ["screen"]
        else:
            self.args = convert_to_list(args)
            
    def _open_files(self):
        """
        Open the files. Can be re-called to solve python BUG issue6333 
        args = ["stdout", "logfile1", "logfile2"] # must be list
        """
        self.FH = []
        for arg in self.args:
            if re.match(self.screen_pattern, arg.lower()):
                self.FH.append(sys.stdout)
            else:
                arg = str(arg)
                if "nt" in os.name:
                    arg = "r'" + arg + "'"
                self._add_FH(arg)
    
    def _dump(self, message_verbosity, message, _where = "ALL"):
        """
        Determines where to write message
        _dump(message_verbose_level, message, [_where = "ALL IS DEFAULT"])
        """
        message = self._add_datestamp(message)
        if  ((message_verbosity) and 
             (self.verbosity >= message_verbosity)) :
            for FH in self.FH:
                if  ("ALL" in _where):
                        print >>FH, message
                if   (("LOG" in _where) and
                      (not re.match(self.screen_pattern, str(FH)))):
                        print >>FH, message      
                if not re.match(self.screen_pattern, str(FH)):
                    os.fsync(FH)

    def close(self):
        for FH in self.FH:
            FH.close()
    
    def out(self, message_verbosity, message):
        """
        User function to send verbose level and messages to object
        obj.dump(verbose_level, message)
        """
        self._dump(message_verbosity, message, _where = "ALL")  
    
    def log(self, message_verbosity, message):
        """
        User function to send message ONLY to established log file(s)
        obj.log(verbose_level, message)
        """
        self._dump(message_verbosity, message, _where = "LOG")  
    
    def screen(self, message_verbosity, message):
        """
        User function to send message ONLY to SCREEN
        obj.screen(verbose_level, message)
        """
        if self.verbosity >= message_verbosity:
            message = self._add_datestamp(message)
            print >>sys.stdout, message
    
    def changeout(self, *args):
        """
        Changes the output devices for the existing object. *args should
        be passed in the same manner as when calling the object initially. 
        """
        self._convert_args_to_list(args)
#        self.close()
        self._open_files()
    
    def changelog(self, *args):
        """
        Changes the LOGFILE output only. If screen already exists as an 
        output, it remains as an ouput. If it is not, it continues to be 
        excluded (unless it has been added as a parameter in the *args
        passed to changelog().
        """
        if  (
             (not re.match(self.screen_pattern, str(args).lower())) and
             (re.match(self.screen_pattern, str(self.args).lower()))
             ):
            args = ("screen",) + args
            self._convert_args_to_list(args)
            self._open_files()
        
    def changelevel(self, level):
        """
        Permanently changes the base verbosity level for the object. 
        """
        try:
            self.verbosity = int(level)
        except ValueError, e:
            e = ("'" + str(level) +  
                 "' is not an integer. \n" + 
                 "Verbosity remains as " + 
                 str(self.verbosity) + "\n" + 
                 str(e))
            raise ValueError(e)
    level = verbosity = changeverbosity = changelevel

    def vout(self):
        def _vout(verbose_level, message):
            self.out(verbose_level, message)
        return _vout
    
    def vlog(self):
        def _vlog(verbose_level, message):
            self.log(verbose_level, message)
        return _vlog
    
    def vprint(self):
        def _vprint(verbose_level, message):
            self.screen(verbose_level, message)
        return _vprint

    def vscreen(self):
        def _vprint(verbose_level, message):
            self.screen(verbose_level, message)
        return _vprint
             
def check_verbose_object(verbose):
    """
    myVerboseOject = check_verbose_object(verbose)
    
    Checks 'verbose' and creates an object usable by a calling script or class.
    
    'verbose' variable can be ...

        An integer which will set the default verbose level for the new 
        myverbose object.
                    
        An existing myverbose object, in which case the object is just passed 
        back into the calling script (checks object). 
        
        None, which creates a default myverbose object with a verbosity of 
        '0' (no output to screen or logs). This is used when a calling script
        does not want, or has no verbose object - but verbose statements exist
        in the script. Will prevent uncallable errors. 
    """
    ### VERBOSE??? Can only be an object, number or None
    if verbose is None:
        # Just create a level 0 (no output) verbose object to avoid errors
        verbose = Verbose()
    else:
        # Check for object 
        if re.match("^.*erbose.*$", str(type(verbose)).lower()):
            # It is an class object, Just pass object into global var
            verbose = verbose 
        else:
            # Check for number
            try:
                verbose = int(verbose)
                # Its a number, create default object
                verbose = Verbose(verbosity=verbose)
            except ValueError, e:
                e = "Variable 'Verbose' passed into __init__ is neither " 
                e = e + "a myverbose object or a integer. "
                raise ValueError(e)
    return verbose

if __name__ == "__main__":
# For development testing only
    o = Verbose(10)
    vout = o.vout()
    vout(10, "test")
    pass # ALWAYS Leave this line to avoid errors
