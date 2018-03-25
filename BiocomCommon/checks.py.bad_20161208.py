##############################################################################
# Removal of the "__license__" line or content from  "__license__", or removal 
# of "__author__" in this or any constituent # component or file constitutes a 
# violation of the licensing and copyright agreement. 
__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = "PERPETUAL_AND_UNLIMITED_LICENSING_TO_THE_CLIENT"
__version__     = "0.9.1.2"
__maintainer__  = "Mike Rightmire"
__email__       = "Mike.Rightmire@BiocomSoftware.com"
__status__      = "Development"
##############################################################################

from math import ceil
from urlparse import urlparse

import inspect
import ntpath
import os.path
import re
import subprocess
import sys
import tempfile

def _check_for_directory_flag(**kwargs):
    if (  kwargs.pop('dir',         False) or
          kwargs.pop('directory',   False) or
          kwargs.pop('folder',      False) 
        ):
        return True
    else:
        return False
    
def _check_for_file_flag(**kwargs):
    if (  kwargs.pop('file',       False) or
          kwargs.pop('filename',   False) 
        ):
        return True
    else:
        return False
        
def _checkSanitized(s, blacklist): # Blackist must be passed in 
    # Check blacklist is list
    if not isinstance(blacklist, list):
        e = ''.join([
            'checks._checkSanitized:',
            "Parameter 'blacklist' must be a list, not '",
            str(type(blacklist)), "'. "
            ])
        raise AttributeError(e)
        
    for word in blacklist:
        word = str(word) # In case blacklist is passed in 
        if re.search(word,s): return False
    
    return True    
    
def _checkLinuxSanitized(s, blacklist = None):
    """"""
    if re.search('[;]', s): return False # ';' common command insertion

    # Blacklist specific to linux        
    if blacklist is None:
        """
        NOTE: THE POSITIONS OF THE SPACES IS CRITICAL HERE.
        Commands are only commands if spaces before and/or after
        Think about spaces here
        """
        # Think about spaces here
        blacklist = [
                       ' rm ', # remove
                       ' -[RrFf]*', # dangerous flags. Note spaces.
                       ' chmod ', # Permissions
                       ' chown ', # Ownership
                       ]

    return _checkSanitized(s, blacklist)
    
def _checkOSXSanitized(s, blacklist = None):
    ### osx specific checks here ###
    return _checkLinuxSanitized(s, blacklist)

def _checkWindowsSanitized(s, blacklist = None):
    raise NotImplementedError()

def _errout(msg, errtype = None):
    if 'exception' in str(errtype).lower():
        raise type(errtype)(msg)
    else:
        raise Exception(msg)
    
def _is(variable, variable_type):
    if 'in' in str(variable_type).lower():
        if isinstance( variable, int ):     return True
        else:                               return False

    elif 'fl' in str(variable_type).lower():
        if isinstance( variable, float ):   return True
        else:                               return False

    elif 'str' in str(variable_type).lower():
        if isinstance( variable, str ):     return True
        else:                               return False
        
    else:
        raise AttributeError("'" + str(variable_type) + "' is not a valid variable check type.")

def _fileExists(path, **kwargs):
    """"""
    # MUST be a full path
    return os.path.isfile(path)

def _dirExists(path, **kwargs):
    return os.path.isdir(path)
 
def _re(p, s, type, *args, **kwargs):
    """"""
    groups      = kwargs.pop('groups', [])
    ignorecase  = kwargs.pop('ignorecase', False)
    
    # check params
    if not isinstance(p, str) or not isinstance(s, str): 
        raise ValueError(''.join(["Both parameters 'p' (pattern) and 's' (string to be searched) must be of type str(). p=(", str(type(p)), ")'", str(p), "', s=(", str(type(s)), ")'", str(s), "'. "]))
    if not isinstance(groups, (list, tuple)): 
        raise ValueError(''.join(["file_utils._check_re_search:",  "Parameter 'groups' ('", str(groups), "') must be a list of integers indicating which matched group items to return. "]))

    # match pattern(p), against string(s)
    if 'm' in str(type).lower():
        if ignorecase:  result = re.match(p,s, re.IGNORECASE)
        else:           result = re.match(p,s)
    # search
    else:
        if ignorecase:  result = re.search(p,s, re.IGNORECASE)
        else:           result = re.search(p,s)

    # If nothing found, return an empty list
    if result is None: return []
    # Returns all
    if ( (groups == []) or ('all' in str(groups).lower()) ): return result.groups()  
    # Else return specific groups
    else:
        list_result = []
        for num in groups:
            try: 
                num = int(num)
                list_result.append(result.group(num))
            except ValueError as e:  raise ValueError(groups_err + '(' + str(e) + ').')
            # Ignore invalid groups indexes
            except IndexError as e:
                pass
#                 msg = ''.join(["Parameter 'groups' index number of '", str(num), "' is not valid [no results.group(", str(num), ") exists]. Skipping. "])
#                 log.warning(msg)
        # Done
        return list_result
 
class Checks(object):
    def __init__(self):
        self._calling_path = os.path.dirname(inspect.getfile(sys._getframe(1)))
        self._calling_file = str(inspect.getfile(sys._getframe(1)))
        self._delim = self.directory_deliminator()
        
    def _makefile(self, path):
        """"""
        _path = str(path)
        # Set starter error message
        err = ''.join(["checks._makefile: '_path' of ", str(_path), " "]) 
        # Check if it looks liek a file
        if len(_path) < 1 or _path.endswith(self.directory_deliminator()) :
            return False
        
        _dir = ntpath.dirname(_path) + self.directory_deliminator()
        _file = ntpath.basename(_path)
        
    #         err = ''.join([err, "Does not appear to be a valid full path with filename. "])
    #         raise ValueError(err)
    
        # Try to make just the directory (and then try to make the file next)
        try:
            _makedir(_dir)
    
        except Exception as e:
            if 'exists':
                pass # If it exists, all is good. 
            
    
            else:
                # Failed to make. Return false
    #             return False
                err = ''.join([err, "Was unable to create directory. ","(", e.message, ")."])
                raise type(e)(err)
        # Make the file itself.     
        try:
            open(_path, 'w+') # Use path not _dir or _file
            return True
        
        except Exception as e:
    #         return False
            err = ''.join([err, "Was unable to create file. ","(", e.message, ")."])
            raise type(e)(err)
    
    def _makedir(self, _path):
        """"""
        _dir = ntpath.dirname(_path)
    #     _dir = _dir + self._delim
        _dir = _dir + self.directory_deliminator()
        try:
            os.mkdir(_dir)
            return True
        
        except Exception as e:
            print e
            return False
    #         err = ''.join(["checks._makedir: Unable to make directory with '", str(_dir), "' (", e.message, ")."])
    #         raise type(e)(err)

    def delimiter(self):
        """
        Just a pointer to directory_deliminator()
        """
        return self.directory_deliminator()

    def directory_delimiter(self):
        """
        Just a pointer to directory_deliminator()
        """
        return self.directory_deliminator()
                      
    def directory_deliminator(self):
        # Check system type and set directory deliminator
        if self.checkOS("windows"): 
            return "\\"
        else: 
            return "/"
                      
    def obfuscate_key(self, _key):
        _key = str(_key)
    
        if len(_key) < 5: return (len(_key) * '*')
        
        _buffer = int(ceil(len(_key) * .2))
        if _buffer > 3: _buffer = 3
    
        _obbedkey = ''.join([
                             _key[:_buffer], 
                             ((len(_key)-(_buffer*2)) * "*"), 
                             _key[len(_key) - (_buffer):]
                             ])
        return _obbedkey
                      
    def checkInt(self, variable):
        return _is(variable, variable_type = 'int')
    checkInteger = checkInt
                      
    def checkFloat(self, variable):
        return _is(variable, variable_type = 'fl')
    checkDecimal = checkDec = checkFloat
                      
    def checkStr(self, variable):
        return _is(variable, variable_type = 'str')
    checkString = checkStr
                      
    def check(self, type, line, *args, **kwargs):
         
        if re.match("^.*path.*$", str(line).lower()):
            fullPathCheck(line) 

    def findExecutablePath(self, exename, expected_path = None, search = True, *args, **kwargs):
            # Linux/OSX try first
            try:
                p = subprocess.Popen(['which', exename],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                _path = p.communicate()[0] # take first component
                if len(_path) > 0:
                    return  ntpath.dirname(_path) + self.directory_delimiter()
                # which did not find.
                if expected_path is not None:
                    p = subprocess.Popen(['ls', expected_path + '\\' + exename],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    _path = p.communicate()[0] # take first component
                    if exename in str(_path):
                        return expected_path
                # ls did not find the exe or no directory at all (wont error)
                if search is True:
                    p = subprocess.Popen(['find', '/','-name',exename],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    _path = p.communicate()[0] # take first component
                if len(_path) > 0:
                    return  ntpath.dirname(_path) + self.directory_delimiter()
                # Never found anything, return None and assume caller will error
                return None
            # If here, one of the commands given to popen was invalid.
            # We will just pass and try again from the assumption it is a windows system. 
            # We can add extra OS here if needed.  
            except (OSError) as e: pass
            
            # Windows
            try:
                p = subprocess.Popen(['where', exename],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                _path = p.communicate()[0] # take first component
                if len(_path) > 0: return  ntpath.dirname(_path) + self.directory_delimiter()
                # where did not find. 
                if expected_path is not None:
                    p = subprocess.Popen(['dir', expected_path + '/' + exename],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    _path = p.communicate()[0] # take first component
                    if exename in str(_path): return expected_path
                # search the system (FUTURE)
                # Something like 
                #===============================================================
                # @echo off & setLocal EnableDELAYedeXpansion
                # 
                # for %%d in (c d e f g h i j k l m n o p q r s t u v w x y z) do (
                #   if exist %%d: (
                #       for /f "tokens=* delims= " %%a in ('dir/b/s %%d:\basecontent.7z 2^>nul') do (
                #         7za.exe x "%%a"
                #       )
                #   )
                # )
                #===============================================================
                
            except WindowsError as e: pass
            
            # Try a different OS here. 
            
            # FINALLY 
            return None
    
    def fullPath(self, path, *args, **kwargs):
        _path = str(path).strip() # REMOVE WHITESPACE FROM ENDS
        
        if not _path.startswith(self._delim):
            # Its relative or just a single word (assuming relative)
            _path = ''.join([ntpath.dirname(self._calling_file), self._delim, _path])
        
        return _path
                      
    def fullPathCheck(self, path, *args, **kwargs):
        """
        INCOMPLETE
        """
        path = str(path)
#         self._delim = self.directory_deliminator()
        if path.endswith(self._delim): _endslash = True
        else:                     _endslash = False
        if (not self.isPathFormat(path, full = True, relative = False, trailing = _endslash)): return False

        return True
    #===============================================================================
    # def checkWindowsPathFormat(_path, endslash = False):
    #     _path = str(_path)
    # 
    #     wp = re.compile("^(([a-zA-Z]:\\\)|(\.\\\)|(\.\.\\\)).*$")
    # 
    #     if not re.match(wp, _path): return False
    # 
    #     if endslash:
    #         if _path[-1:] == "\\": return True
    #         else: return False
    #     
    # def checkLinuxPathFormat(_path, endslash = False):
    #     _path = str(_path)
    #     
    #     lp = re.compile("^((\./)|(\.\./)|(/)).*$")
    # 
    #     if not re.match(lp, _path): return False
    #     
    #     #Must come after re.match
    #     if endslash:
    #         if _path[-1:] == "/": return True
    #         else: return False
    #===============================================================================
    
    #===============================================================================
    # def checkPathFormat(path, full = False, relative = False, trailing = False):
    #     return isPathFormat(path, full = False, relative = False, trailing = False)
    # #     _path = str(_path)
    # #     if   checkWindowsPathFormat(_path, endslash): return True
    # #     elif checkLinuxPathFormat(_path, endslash)  : return True
    # #     else: return False
    #===============================================================================
        
    def pathExists(self, path, **kwargs): #create = False, full = True, relative = False, trailing = False, **kwargs):
        """
        Check that a full path exists when ONLY the full path is path
        
        This differs from directoryExists, which checks (ONLY) that the full path 
        exists when path is the full path PLUS THE FILENAME. 
        """
        _calling_path = os.path.dirname(inspect.getfile(sys._getframe(1)))
        _calling_file = str(inspect.getfile(sys._getframe(1)))
        _path = str(path).strip() # Remove whitespaces
#         _delim = self.directory_deliminator()
        _result = False # Negative assumption
        _dir = _check_for_directory_flag(**kwargs)
        _file = _check_for_file_flag(**kwargs)
        _create = kwargs.pop('create', False)
        #Check if relative, make full if it is. Use the calling files path
        _path = self.fullPath(path)
        # At this point, we should have a full path in one form
        # Check for both a dir and a file. If neither return False
        
        #=======================================================================
        # print 'At os.path.exists...'
        # print "_path =", _path #333
        # print "_file =", _file #3333
        # print "_dir = ", _dir #333
        #=======================================================================
        
        _expanded_path = os.path.expanduser(_path) # Fixes spaces in dir problem
        if os.path.exists(_expanded_path): # path exists as either file or dir
#         if os.path.exists(_path): # path exists as either file or dir
            if _file  : return _fileExists(_path) # Check specifically file
            elif _dir : return _dirExists(_path) # Check specifically dir
            else      : return True

        else: # Does not exists, cheack for create
            if _create: # Default False
                if _dir     : return self._makedir(_path)
                elif _file  : return self._makefile(_path)
                else        :
                    err = ''.join(["Checks.pathExists.create: ", "The 'create' param muct be accompanied by a 'directory = True' or 'file = True' flag. "])
                    raise ValueError(err)
        
            else: # Create = False, return False
                return False
                      
    def fullPathExists(self, path, **kwargs): #create = False, full = True, relative = False, trailing = False):
        return self.pathExists(path, **kwargs)
#===============================================================================
#         """
#         :NAME:
#             fullPathExists(path)
#     
#         :DESCRIPTION:
#             Intended to check the existence of ONLY the path assuming a full path
#             with filename included is passed.
#             
#             This differs from pathExists, which checks that the full path 
#             exists when _path is the full path WITHOUT THE FILENAME.
#             
#             fullPathExists ONLY checks that the path exists. NOT the filename.
#      
#     
#         :ARGUMENTS:
#             path:    The full path WITH FILNEMAE I.e "/dir1/dir2/filename.ext"
#             create:  (True/False) If path does NOT exist, but create is True,
#                      path will be created and True returned. 
#         :USAGE:
#             if fullPathExists("/dir1/dir2/filename.ext"):
#                 print "The directory is there. I haven't check for the filename".
#             else:
#                 print "'/dir1/dir2' does not exist."
#         """
#         path = str(path)
#         if not Checks.isPathFormat(path, full = True, relative = relative, trailing = trailing): return False
# 
#         if trailing is True:
#         # it is a path not a filename    
#             if Checks.pathExists(path): return True
#             elif create is True:        return _makedir(path) # Returns True/False
#             else:                       return False
#         else: 
#         # No trailing implies filename not directoryname
#             if Checks.fileExists(path): return True
#             elif create:                return Checks._makefile(path)
#             else:                       return False
#             
#         # Something went wrong if here
#         err = ''.join(["Checks.fullPathExists: ", "Unable to properly complete process. Please debug Checks."])
#         raise Exception(err)
#===============================================================================
                
    #=============================================================================
    #=============================================================================
    # DEPRICATED. USE fullPathExists            
    # def directoryExists(_path, create = False): # This name needs to be depricated
    #     """
    #     :NAME:
    #         directoryExists(path)
    # 
    #     :DESCRIPTION:
    #         Intended to check the existence of ONLY the path assuming a full path
    #         with filename included is passed.
    #         
    #         This differs from pathExists, which checks that the full path 
    #         exists when _path is the full path WITHOUT THE FILENAME.
    #         
    #         directoryExists ONLY checks that the path exists. NOT the filename.
    #  
    # 
    #     :ARGUMENTS:
    #         path:    The full path WITH FILNEMAE I.e "/dir1/dir2/filename.ext"
    #         create:  (True/False) If path does NOT exist, but create is True,
    #                  path will be created and True returned. 
    #     :USAGE:
    #         if directoryExists("/dir1/dir2/filename.ext"):
    #             print "The directory is there. I haven't check for the filename".
    #         else:
    #             print "'/dir1/dir2' does not exist."
    #     """
    #     _path = str(_path)
    #     _path = os.path.dirname(_path)
    #     
    #     if pathExists(_path):
    #         return True
    #     
    #     else:
    #         if create == True:
    #             try:
    #                 os.makedirs(_path)
    #                 return True
    # 
    #             except Exception as e:
    #                 return False
    # #                 e.message = ''.join(["From 'checks.directoryExists()': ", 
    # #                                      "Directory '", 
    # #                                      str(_path), 
    # #                                      "' does not exist and an error occurred ", 
    # #                                      "trying to create it. ", 
    # #                                      e.message])
    # #                 raise type(e)(e.message)                
    #             
    #         else:
    #             return False
    #         
    # #     return pathExists(_path)
    #=============================================================================
    #=============================================================================
                      
    def fileExists(self, file, *args, **kwargs):
        """
        :NAME:
            fileExists(file, [*args, **kwargs])
        
        :PARAMETERS:
            file:   Path and filename
            
            create: If True, create a blank file by filename
            
        :DESCRIPTION:
            Returns True if file exists
            
            If file does not exist but 'create' is True, will attempt to create 
            a blank file at /path/name
            
            Otherwise retruns False
        """
        _file = str(file)
        if _fileExists(_file):            return True
        elif kwargs.pop('create', False): return self._makefile(_file) 
        else:                             return False
    isFile = fileExists

    def directoryExists(self, directory, *args, **kwargs):
        """
        :NAME:
            directoryExists(directory, [*args, **kwargs])
        
        :PARAMETERS:
            directory:   Path and filename
            
            create: If True, create a blank directory by said name
            
        :DESCRIPTION:
            Returns True if directory exists
            
            If directory does not exist but 'create' is True, will attempt to create 
            a blank directory at /path/name
            
            Otherwise returns False
        """
        _directory = str(directory)
        if _dirExists(_directory):            return True
        elif kwargs.pop('create', False): return self._makedir(_directory) 
        else:                             return False
    isdirectory = isDir = directoryExists

    #===============================================================================
    # def verifyLogfile(logfile, create = False):
    #     """"""
    #     _logfile_default = 'syslog'
    #     _test = str(logfile).lower()
    # 
    #     if (
    #         (logfile is None)   or 
    #         (_test) < 1)        or
    #         (_test == 'none')   or
    #         (_test == 'void')   or
    #         (_test == 'syslog')
    #         ): 
    #         return _logfile_default
    #     
    #     #===========================================================================
    #     # # If here, the logfile passed is a path and/or filename
    #     # # Strip illegal characters
    #     # # This automatically converts what was passed into a string
    #     # logfile = (''.join(c for c in str(logfile) if re.match("[a-zA-z0-9 -_./\\ ]", c)))
    #     #===========================================================================
    # 
    # 
    #     # Check that directory exists and, if not, create it 
    # #         if not directoryExists(logfile, create = self.create_paths):
    #     if not pathExists(logfile, create = self.create_paths):
    #         err = ''.join(["The logfile directory '",str(logfile),"' does not exist and creating it either ","failed or is prohibited by the 'create_paths' ", " parameter (currently set as '", str(self.create_paths), "')."])
    #         raise AttributeError(err)
    # 
    #     return os.path.abspath(logfile)
    #===============================================================================
                      
    def checkServername(self, _name):
        if len(_name) < 1: return False
        if re.match("^[a-zA-Z0-9-]*$", str(_name)): return True
        if checkIP(_name): return True
        else: return False
                      
    def checkIP(self, IP):
        """"""
        IP = str(IP)
        IP = IP.lstrip()
        IP = IP.rstrip()
        
        pattern = (''.join([ "^", "(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})" "$"]))
        pattern = re.compile(pattern, re.IGNORECASE)
    
        if pattern.match(IP):   return True
        else:                   return False
                      
    def checkURI(self, URL = None, URI = None, *args, **kwargs):
        """
        :NAME:
            checkURI(URL = STRING/None, URI = STRING/None [, *args, **kwargs])
        
        :DESCRIPTION:
            Returns True or False if string is a validly formatted URL/URI
        
        :PARAMETERS:
            URL: (String) A URL in the format:
                 http://www.google.com/somewhere
                
            URI: (String) A URI in the format:
                 <scheme>://main/sub
                 s3://dev.myserver.com/dir/dir/file.ext
        
        :USAGE:
            import Checks
            checks = Checks()
            if checks.checkURI('s3://dev.myserver.com/dir/dir/file.ext'):
                print 'It is Valid'
            else:
                print 'It is invalid'
        """
        if URL is None: 
            if URI is None:
                return False
            else:
                URL = URI
                
        URL = str(URL)
        URL = URL.strip()
        #=======================================================================
        # pattern = ("^(https?){0,1}"        +               # http/https
        #             "(://){0,1}"            +               # ://
        #             "(\w+\.){0,}" +                  # Prefix [I.e. www.] (Optional)
        #             "((\w+)(\.\w\w+)"    +   # Server.xx (mandatory)
        #             "|" +                            # servername OR IP
        #             "(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))" + # OR IP (mandatory)  
        #             "(:\d+){0,1}" + # port (mandatory)
        #             "(\/\.*){0,}"    +   # remainder
        #            "$")
        # 
        #=======================================================================
        
        pattern = "^([a-z0-9+.-]+):(?://(?:((?:[a-z0-9-._~!$&'()*+,;=:]|%[0-9A-F]{2})*)@)?((?:[a-z0-9-._~!$&'()*+,;=]|%[0-9A-F]{2})*)(?::(\d*))?(/(?:[a-z0-9-._~!$&'()*+,;=:@/]|%[0-9A-F]{2})*)?|(/?(?:[a-z0-9-._~!$&'()*+,;=:@]|%[0-9A-F]{2})+(?:[a-z0-9-._~!$&'()*+,;=:@/]|%[0-9A-F]{2})*)?)(?:\?((?:[a-z0-9-._~!$&'()*+,;=:/?@]|%[0-9A-F]{2})*))?(?:#((?:[a-z0-9-._~!$&'()*+,;=:/?@]|%[0-9A-F]{2})*))?$"

        pattern = re.compile(pattern, re.IGNORECASE)
     
        if pattern.match(URL): return True
     
        #=======================================================================
        # elif re.match("^\s*(https?://){0,1}localhost\s*[/\.]{0,}$", str(URL), re.IGNORECASE):
        #     return True
        #=======================================================================
        #=======================================================================
        # #These are specific to the urlparse method
        # scheme          = kwargs.pop('scheme', None)
        # allow_fragments = kwargs.pop('allow_fragments', None)
        # 
        # if urlparse(URL, scheme, allow_fragments): return True
        #=======================================================================
        else:
            # If error was passed in as True, then raise error on failure
            if kwargs.pop('error', False):
                err = ''.join(["URL/URI:'", str(URL), "' does not match expected format."])        
                raise NameError(e)
            # Otherwise just return False
            return False
    # Map old for compatibility
    checkURL = checkURI
                      
    def checkS3(self, URI):
         # check for white spaces
        p = '\s'
        if re.search(p, URI): return False # check for white spaces
    
        # Check overall structure
        p = ("^(s3://)" +         # s3 header 
             "([^/]*)"  +         # Bucket name
             "((/*\S{1,})*[^/])$" # Everything else, do not end in '/'
             )
        _re = re.compile(p, re.IGNORECASE | re.UNICODE)
        match = _re.match(ORIGINAL_S3PATH)
        if not match: return False
        
        return True
            
    def checkOS(self, os = None):
        """
        checkOS(['os'])
        
        DESCRIPTION
            checkOS returns either the OS platform (if called with no option), 
            or a True/False if the passed option matches the OS type.
            
        OPTIONS
            os = a STRING containing the name of the os to be identified. If the 
                 platform matches the 'os', checkOS will return True, 
                 otherwise it returns False.
                 
                Acceptable 'os' parameters are:
                    windows = T if windows OS
                    win     = T if windows OS
                    win32   = T if windows 32 bit specifically
                    win64   = T if windows 64 bit specifically
                    freebsd = T if FreeBSD specifically
                    gnu     = T if GNU OS specifically
                    linux   = T if linux, or GNU, or FreeBAD
                    unix    = T if Solaris, or riscos, or FreeBSD
                    *nix    = T if linux, or GNU, or FreeBAD, or Solaris, 
                              or riscos, or FreeBSD
                    risc    = T is riscos
                    atheos  = T is atheos
                    solaris = T if solaris, or sunos
        """
        def _windows_os():
            if sys.platform.startswith('win'): return True
            else: return False

        def _windows32_os():
            if str(sys.platform) == "win32":  return True
            return False

        def _windows64_os():
            if str(sys.platform) == "win64": return True
            return False
        
        def _linux_os():
            if sys.platform.startswith('linux'): return True
            if _gnu_os(): return True
            if _freebsd_os: return True
            if _osx_os(): return True
            return False
            
        def _osx_os():
            if sys.platform.startswith('darwin'): return True
            else: return False                
        
        def _cygwin_os():
            if sys.platform.startswith('cygwin'): return True
            else: return False
            
        def _os2_os():
            if sys.platform.startswith('os2'): return True
            else: return False
            
        def _os2emx_os():
            if sys.platform.startswith('os2emx'): return True
            else: return False
            
        def _riscos_os():
            if sys.platform.startswith('riscos'): return True
            else: return False
            
        def _atheos_os():
            if sys.platform.startswith('atheos'): return True
            else: return False                
    
        def _sun_os():
            if sys.platform.startswith('sunos'): return True
            else: return False
                    
        def _freebsd_os():
            if sys.platform.startswith('freebsd'): return True
            else: return False
    
        def _gnu_os():
            if sys.platform.startswith('gnu'): return True
            else: return False

        def _unix_os():
            if _freebsd_os(): return True
            if _sun_os(): return True
            if _riscos_os():  return True
            return False

        def _nix_os():
            if _freebsd_os(): return True
            if _sun_os(): return True
            if _riscos_os(): return True
            if _linux_os(): return True
            if _gnu_os(): return True
            if _osx_os(): return True
            if _cygwin_os(): return True
            return False
                                                                        
        def _unknown_os():
            return sys.platform    
    
        _os = str(os).lower()
        
        if os is None: return sys.platform
        if sys.platform == _os: return True
                
        return {
                "win"       :_windows_os,
                "w"         :_windows_os,
                "windows"   :_windows_os,

                "win32"     :_windows32_os,
                "w32"       :_windows32_os,
                "x32"       :_windows32_os,

                "windows32" :_windows32_os,
                "win64"     :_windows64_os,
                "w64"       :_windows64_os,
                "x64"       :_windows64_os,
                "ia64"      :_windows64_os,
                "windows64" :_windows64_os,
                 
                "g"         :_gnu_os, 
                "gnu"       :_gnu_os,

                "lin"       :_linux_os, 
                "l"         :_linux_os,
                "linux"     :_linux_os,
                
                "freebsd"   :_freebsd_os,
                "free"      :_freebsd_os,
                "bsd"       :_freebsd_os,
                
                "mac"       :_osx_os,
                "osx"       :_osx_os,
                "darwin"    :_osx_os,
                "dar"       :_osx_os,
                "apple"     :_osx_os, 
                
                "cygwin"    :_cygwin_os,
                "cyg"       :_cygwin_os,
                "c"         :_cygwin_os,
                          
                "os2emx"    :_os2emx_os,
                "emx"       :_os2emx_os,
                    
                "os2"       :_os2_os,
                    
                "risc"      :_riscos_os,
                "riscos"    :_riscos_os,
                    
                "atheos"    :_atheos_os,
                "athe"      :_atheos_os,
                "ath"       :_atheos_os,        
                        
                "solaris"   :_sun_os,
                'sol'       :_sun_os,
                'sun'       :_sun_os,
                        
                'unix'      :_unix_os,
                'nix'       :_nix_os,
                '*nix'      :_nix_os,
                
                }.get(_os)()
        # Nothing matched. error basically
#         return False
        err = ''.join([self.__class__.__name__, ".", inspect.stack()[0][3], ": ", 
                       "Unable o successfully match an OS. Erroring out instead of passing a False back. "])
        raise OSError(err)
                      
    def checkSanitized(self, s, blacklist = None):
        """
        :NAME:
            checkSanitized(<string>, blacklist = [<list of strings>])
            
        :DESCRIPTION:
            checkSanitized() will check the passed-in string for potential security 
            risk keywords. If 'blacklist' is not passed, it will use a default
            list of keyword risks (recommended) appropriate to the operating system. 
            Passing in a 'blacklist' requires a deep understanding of the mechanisms 
            of checkSanitized() and of how regex searches are performed, and is 
            not recommended.  
            
            checkSanitized() returns True (no risks, string is sanitized) or 
            False (risks found).
            
            The check is done via a regex 'search' function, meaning any appearance 
            of the keyword in the string will return a 'False' response. This means
            traditional regex expressions can be included, and spaces are critical 
            when creating a blacklist keyword. 
            
            For example, searching for specific words as 'rm' is different than 
            ' rm '. Consider the string 'charactermove' (containing 'rm') which 
            does not contain a risk) versus the string 'rm passwd' 
            (containing 'rm ') which is unquestionably a risk.
            
            Default risk keywords include ';' and other database related concerns 
            such as 'drop ', 'insert ', 'delete '. When using checkSanitized() to 
            check select statements for databases, a blacklist must be passed in
            which overrides all defaults including these. 
            
        :ARGUMENTS:
            <string>:   A string to be checked. If a non-string is passed, it will
                        be converted to a string and checked. 
                        
            blacklist:  A list of strings to be used as keywords against which the 
                        string will be checked. Full regex expressions can be used
                        as individual string keywords within this list. SPACES
                        within keywords ARE NOT IGNORED, meaning 'rm' and 'rm ' will
                        produce different results.   
    
                        Default risk keywords include ';' and other database related 
                        concerns such as 'drop ', 'insert ', 'delete '. When using 
                        checkSanitized() to check select statements for databases, 
                        a blacklist must be passed in which overrides all defaults 
                        including these. 
    
        :RETURNS:
            True or False
            
        :USAGE:
            s = 'my text string'
            if checkSanitized(s):
                <continue with code>
            else:
                <raise error message>
        """    
        _os = self.checkOS()
        s = str(s)
        
        # Check the always sanitized stuff
        # If blacklist is NOT NONE, then dont do this
        if blacklist is None:
            """
            NOTE: THE POSITIONS OF THE SPACES IS CRITICAL HERE.
            Commands are only commands if spaces before and/or after
            Think about spaces here
            """
            # Think about spaces here
            _blacklist = [
                         ' delete ', # General
                         ' drop ' ,# Database
                         ' insert ', # Database
                        ]
            
            # Return here. No need to continue if failes. 
            if (_checkSanitized(s, _blacklist) is False): return False
            
        # These get run regardless of blacklist = None
        
        if   checkOS('linux2')  : return _checkLinuxSanitized(s, blacklist)
        elif checkOS('win')     : return _checkWindowsSanitized(s, blacklist)
        elif checkOS('darwin')  : return _checkOSXSanitized(s, blacklist)
        else:
            err = ''.join([
                           "checks.checkSanitized: ", 
                           "Unable to sanitize for operating system '", 
                           str(_os),
                           "'."
                           ]) 
                           
            raise AttributeError(err)
    
    #===============================================================================
    # def checkTempdir(_dir, create = False):
    #     """
    #     Checks the existence of the temp directory passed in. 
    #     If directory exists, returns the directory name. (No True/False)
    #     If it doesn't exist, create = True attempts to create it. 
    #     Must give FULL DIRECTORY PATH
    #     Raises error on failure (No True/False)
    #     """
    #     err_does_not_exist = ''.join(["Directory:'", str(_dir), "' ", 
    #                                   "does not exist."])
    #     
    #     err_cannot_create = ''.join(["Unable to create ", 
    #                                  "the .temp directory:'", str(_dir),  "'.", 
    #                                  ])
    # 
    #     err_not_full_path = ''.join(["Directory:'", str(_dir), "' ", 
    #                                   "does not appear to be a full path."])
    #     
    #     if _dir is None: 
    #         raise ValueError(err_not_full_path)
    #     else:
    #         _dir = ''.join(c for c in str(_dir) if c not in '     ')
    #     
    #     if _dir.lower() == 'system':
    #         raise NotImplementedError('Use of system temp directory not yet implemented.')
    # 
    #     if ((not _dir.startswith(delim())) or (not _dir.endswith(delim()))):    
    #         raise ValueError(err_not_full_path)
    #         
    #     _dir = check_directory_format(_dir)
    #     
    #     if ntpath.exists(_dir): 
    #         return _dir
    # 
    #     else:
    #         if create:
    #             try:
    #                 os.makedirs(_dir)
    #                 return _dir
    #             except Exception as e:
    #                 raise type(e)(e.message + 
    #                               err_cannot_create + 
    #                               "Please check the path and  permissions. ")                
    #         else:
    #             raise IOError(err_does_not_exist + "create = False.")                
    #===============================================================================
                      
    def isDict(self, _dict):
        try:
            _dict.keys()
            return True
        except (AttributeError):
            return False
    checkDict = isDict
                      
    def isList(self, _list):
        try:
            _list.append("DELETEMELISTCHECKVARIABLE")
            _list.pop(len(_list)-1)
        except AttributeError, e:
            return False
        except Exception, e:
            raise
        return True
    checklist = isList
                      
    def isObject(self, obj):
        if (
            ("object" in str(obj).lower()) or
            ("instance" in str(obj).lower())
             ):
            return True
        else:
            return False
    checkObject = isObject
                      
    def isPathFormat(self, path, full = False, relative = False, trailing = False):
        """
        :NAME:
        isPathFormat(path, [full = False, relative = False, trailing = False])
        
        :DESCRIPTION:
        Checks if the format of a string is consistent with the OS's path format. 
        Does not check whether the path exists.
        This implicitly verifies the correct OS is checked for 
        """
#         _delim = self.directory_deliminator()
        path = str(path)
        # Build directory forbidden character list, as a [anyof]
        invalid_chars = ''.join([
                    "[",
                    "\<", # (less than)
                    "\>", # (greater than)
                    "\:", # (colon)
                    '\\\"', # (double quote)
                    "\\\'", # (Single quote)
                    "\|", # (vertical bar or pipe)
                    "\?", # (question mark)
                    "\*", # (asterisk)   
                    "\s", # space chars                
                     ])
    
        # Add the opposite OS directory delimiter
        if "/" in self._delim: invalid_chars = invalid_chars + "\\\\"
        else:             invalid_chars = invalid_chars + "/"
        
        #Finish it off
        invalid_chars = invalid_chars + "]"
        
        # Check for forbidden characters
        if re.search(invalid_chars, path): return False
        # If here, all chars are legal. Just check start and finish
        # If full path is required, start with first
        if (full) and (not path.startswith(self._delim)):
#             print 'checks.isPathFormat:FALSE not startswith', _delim #3333 
            return False
        # if relative, must start with dot slash
        if (relative) and (not path.startswith("." + self._delim)):
#             print 'checks.isPathFormat:FALSE not  . and ', _delim #3333 
            return False
        # If trailing the a trailing delimiter is required
        if (trailing) and (not path.endswith(self._delim)):
#             print 'checks.isPathFormat:FALSE not endswith', _delim #3333 
            return False
        # Otherwise, if here, everything aligns
        return True
        
    #===============================================================================
    #     p = re.compile("^(([a-zA-Z]:\\\)|(\.\\\)|(\.\.\\\)).*$")
    # 
    #     _path = str(_path)
    #     _delim = directory_deliminator()
    #     
    #     if re.search(" ", _path): return False
    #     
    #     if not _path.endswith(_delim): _path = ntpath.dirname(_path) + _delim
    #     
    #     if ( 
    #         ( (_path.startswith('.')) or (_path.startswith(_delim)) ) and 
    #         (_path.endswith(_delim)) 
    #        ):
    #         return True 
    #     else:
    #         return False
    #===============================================================================
    checkPathFormat = isPathFormat

    def re_match(self, p, s, *args, **kwargs):
        return _re(p, s, 'match', *args, **kwargs)        

    def re_search(self, p, s, *args, **kwargs):
        return _re(p, s, 'search', *args, **kwargs)        


if __name__ == "__main__":
    o = Checks()
    p = '(This)(.*)(is)(.*)(a)(.*)(test)(.*)'
    s = 'Holy moly This is a great big test'
    print o.re_search(p,s, groups = [2,4, 18])