#!/usr/bin/python
##############################################################################
# Removal of the "__license__" line or content from  "__license__", or removal 
# of "__author__" in this or any constituent # component or file constitutes a 
# violation of the licensing and copyright agreement. 
__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = "BioCom_Commercial_Copyright.py"
__version__     = "0.9.0.0"
__maintainer__  = "Mike Rightmire"
__email__       = "rightmirem@utr.net"
__status__      = "Test"
##############################################################################

from checkos import *
import logging
import logging.handlers
import pywintypes
import re

def verbose(self, 
    app, logfile = None, loglevel = 40, screen = False, rotation = None, 
    host = None, port = None, udp = None, encoding = None, delay = None, 
    backupCount = 0, httpPost = "Get", mailHost = None, 
    toEmail = None, fromEmail = None, facility = None, credentials=None, 
    secure=None, buffer = None):
    """
    Method
        verbose(self, [optional arguments])
        
        verbose is intended to create log objects for use within other classes.
        
        "self" needs to be passed to this method just as if it were a local 
        method to the calling class. Four log variables are created when this 
        method is called...
        
        self.vout   = Log messages go to all configured log paths (self.vprint, 
                      self.log AND self.vnet)
                      
        self.vprint = Dumps the formatted log message to the screen, regardless
                      of whether screen has been added to the general log path.

        self.vlog   = Formatted messages go to the configured file logs only. 
        
        self.vnet   = Formatted messages go to the configured network log 
                      only (http, TCP socket, DGRM socket, etc).
    Method Arguments
        app      =  Name of the class or application
    
        logfile  =  The file to write error messages to. 
    
                    "sys" will send log output to the system OS default log
                        I.e. linux syslog or windows application event
                        
                    An HTTP address means logging will go to a web server
    
                    None or "" means file logging is OFF
    
        loglevel  = The default level to log based on the python "logging" 
                    module I.e. debug, info, error, etc.
                    If unspecified, the default level of error (40) is used 
    
        screen    = Set error output to screen on (True) or off (False). 
                    False (OFF) is the default. 
                    WARNING: If you set screen to False AND fail to pass in a 
                    valid logfile, you can create a condition where all errors
                    and logging are off and the program can end silently. 
                    
        rotation  = Placeholder for log file rotation parameters. 
                    
                        <numeric> = the file size at which rotation will occur
                        s/m/h/d + number = the file rotation schedule based on 
                                time (see the documentation for 
                                logging.handlers.TimedRotatingFileHandler
                                for details.
                    
                        If rotation is None, log file will be called using
                        logging.handlers.WatchedFileHandler 
                                
        host, port= Placeholder. If included, will create a logger which sends
                    data to a network socket.
        
        udp       = Placeholder. If set to True IN CONJUNCTION with host and 
                    port, UDP (datagram) will be used with the network socket 
                    instead of TCP (stream).
        
        toEmail
        fromEmail
        mailHost  = Placeholder. If ALL THREE ARE SET TO Non-Nullm an email is 
                    included and is a valid logging point (the log line is 
                    emailed.)
                    
                    If 'Buffer' is included, this will indictae how many log
                    lines to include in the email before sending.  

                    CAUTION: ALL LOG MESSAGES TRIGGERED WILL GO TO THE EMAIL. 
                             INADVERTENTLY SETTING THIS WITH A LOGGING LEVEL OF 
                             "DEBUG" OR "INFO" COULD HAVE DISASTEROUS RESULTS ON 
                             YOUR MAIL SERVER! 
        
        httpPost  = If logfile is set to a valid http address, this will set 
                    whether "get" or "post" is used. Unspecified is "Get"
                    
        backupCount = Same as in the logging documentation. Default = 0
        
        facility  = Same as in the logging documentation. Default = None
        
        credentials= Same as in the logging documentation. Default = None 
    secure=None, buffer = None
    """

# verbose  will set only 4 types of loggers, which are set based on the 
# different options available from the "logging" module: 
#     vout   = logs to EVERYTHING (file, screen, net)
#     vprint = logs only to screen
#     vlog   = logs only to file (as set by parameters)
#     vnet   = logs only to any network logging (as set by parameters)

    def _try_local_logfile(logfile):
        # local = open logfile in running directory
        if str(logfile).lower() == "local":
            logfile = str(self.__class__.__name__) + ".log"
            _set_file_handler(logfile)
            return True
        else: 
            return False
        
    def _try_syslog_logfile(logfile):
        # Sys = log to the default OS syslog
        if str(logfile).lower() == "syslog":
            if   windows_os: 
                _set_windows_handler()
                return True
            elif linux_os:   
                _set_linux_handler()
                return True
            elif osx_os:     
                _set_osx_handler()
                return True
            else:
                return False
        return False
        
    def _try_file_logfile(logfile, rotation):
        winp    = "^\S(:)(\\\){1}.+$"   # Pattern for windows files
        linuxp  = "^(/[a-zA-Z \"\'\.]*)*$" # Pattern for linux files
        
        # If they match file paths, try to open them
        if (    (re.match(winp, logfile)) or 
                (re.match(linuxp, logfile))
            ):

            # no rotation = simple watched file handler 
            if rotation is None:
                _set_watchedfile_handler(logfile)
                return True

            else:
                _try_rotation_logfile(logfile)
                return True

            return False

    def _try_rotation_logfile(logfile, rotation):
        # See if rotation is set to an int meaning a max file size
        try:
            maxBytes = int(rotation) # errors if not a whole number
            _set_rotatingfile_handler(logfile, maxBytes)
            return True
        except ValueError, e:
            _try_timedrotation_logfile(logfile, rotation)
            return True
        return False

    def _try_timedrotation_logfile(logfile, rotation):
        base = rotation
        ptime       = "^([sSmMhHdD]{1}\d+)$"
        pweekday    = "^([wW]{1}[0-6]{1})$"
        pmidnight   = "^([mM][iI][dD][nN][iI][gG][hH][tT])$"
        e = ("Invalid parameter 'rotation' passed ('" + str(rotation) + ")'")

        # Check if by time (s/m/h/d + 1234)
        if re.match(ptime, str(base)):
            base = "".join(c for c in base if c in "sSmMhHdD")
            time = int("".join(n for n in base if n in '0123456789'))
            _set_timedrotatingfile_handler(logfile, base, time)
            return True

        # Check if by weekdays (w0-w6)
        elif re.match(pweekday, str(base)):
            base = int("".join(n for n in base if n in '0123456789'))
            if base > 6:
                # Raise error not return false, because weekday 
                # ("w<somenumber>") WAS passed but incorrectly formatted
                raise ValueError(e)
            else:
                base = "w" + str(base)
                _set_timedrotatingfile_handler(logfile, base, 0)
                return True
            
        # Check if at "midnight" every night
        elif  re.match(pmidnight, str(base)):
            _set_timedrotatingfile_handler(logfile, "midnight", 0)
            return True
        
        # Doesn't match
        else:
            return False

    def _try_mail_logfile(logfile):
        e = "Will be implemented in a future release"
        raise NotImplementedError(e)
    
    def _try_memory_logfile(logfile):
        e = "Will be implemented in a future release"
        raise NotImplementedError(e)

    def _try_web_logfile(logfile):
        e = "Will be implemented in a future release"
        raise NotImplementedError(e)
    
    def _try_socket_logfile(logfile):
        e = "Will be implemented in a future release"
        raise NotImplementedError(e)

    def _try_dgram_logfile(logfile):
        e = "Will be implemented in a future release"
        raise NotImplementedError(e)
                
    def _set_logfile(logfile):
        if   _try_local_logfile(logfile):         return 
        elif _try_syslog_logfile(logfile):        return 
        elif _try_file_logfile(logfile, rotation):return
        else:
            e = ("Unable to match parameter 'logfile' (" + 
                 str(logfile) + ") to a valid log handling method.")
            raise ValueError(e)         
#         elif _try_mail_logfile(logfile):          return
#         elif _try_memory_logfile(logfile):        return
#         elif _try_web_logfile(logfile):           return
#         elif _try_socket_logfile(logfile):        return
#         elif _try_dgram_logfile(logfile):         return
#         else:
#             e = ("Unable to match parameter 'logfile' (" + 
#                  str(logfile) + ") to a valid log handling method.")
#             raise ValueError(e)

    def _set_screen_handler():
        # Always set a screen handler
        try:
            handler_screen = logging.StreamHandler()
            handler_screen.setFormatter(formatter)
            self.vprint.addHandler(handler_screen)
            # Add the screen to the vout only if param 'screen' == True
            if screen: self.vout.addHandler(handler_screen)
        except Exception, e:
            raise
        
    def _set_windows_handler():
        try:
            handler_windows = logging.handlers.NTEventLogHandler(
                app, dllname=None, logtype='Application')
            handler_windows.setFormatter(formatter)
            _add_log_handler(handler_windows)
        except pywintypes.error, e:
            if 'RegSetValueEx' in str(e):
                e = ("Error A write error has occurred " + 
                     "attempting to write Event Viewer (Windows Application log) " + 
                     "entry to registry. " + 
                     "This can happen if the application using the verbose " + 
                     "logger is running as a user that does not have " + 
                     "permissions. Try running the application as a specific " + 
                     "user, as system, or as Administrator."  + str(e) )
                raise pywintypes.error(e)
            else:
                raise
            
    def _set_linux_handler():
        try:
            if port is None: port = 514
            handler_linux = logging.handlers.SysLogHandler(
                address=('localhost', port))
            handler_linux.setFormatter(formatter)
            _add_log_handler(handler_linux)
        except IOError, e:
            if 'filename' in str(e):
                e = ("You may want to try escaping your logfile name with " + 
                     "an 'r' (raw). " + str(e))
                raise IOError(e)
            else:
                raise
        except Exception, e:
            raise
        
    def _set_osx_handler():
        e = "Will be implemented in a future release"
        raise NotImplementedError(e)
#         logfile = str(__class__.__name__) + ".log"
#         _set_file_handler(logfile)
#         .setFormatter(formatter)
#         _add_log_handler()
                        
    def _set_null_handler():
        try:
            handler_null = logging.NullHandler()
            self.vout.addHandler(handler_null)
            self.vlog.addHandler(handler_null)
            self.vnet.addHandler(handler_null)
        except Exception, e:
            raise
        
    def _set_file_handler(logfile):
        try:
            handler_file = logging.FileHandler(logfile)
            handler_file.setFormatter(formatter)
            _add_log_handler(handler_file)
        except IOError, e:
            if 'filename' in str(e):
                e = ("You may want to try escaping your logfile name with " + 
                     "an 'r' (raw). " + str(e))
                raise IOError(e)
            else:
                raise
        except Exception, e:
            raise
        
    def _set_watchedfile_handler(logfile):
        try:
            handler_watchedfile = logging.handlers.WatchedFileHandler(logfile)
            handler_watchedfile.setFormatter(formatter)
            _add_log_handler(handler_watchedfile)
        except IOError, e:
            if 'filename' in str(e):
                e = ("You may want to try escaping your logfile name with " + 
                     "an 'r' (raw). " + str(e))
                raise IOError(e)
            else:
                raise
        except Exception, e:
            raise
        
    def _set_rotatingfile_handler(logfile, size):
        try:
            handler_rotatingfile = logging.handlers.RotatingFileHandler(
                logfile, mode='a', maxBytes=size, backupCount=0, encoding=None, 
                delay=0)
            handler_rotatingfile.setFormatter(formatter)
            _add_log_handler(handler_rotatingfile)
        except IOError, e:
            if 'filename' in str(e):
                e = ("You may want to try escaping your logfile name with " + 
                     "an 'r' (raw). " + str(e))
                raise IOError(e)
            else:
                raise
        except Exception, e:
            raise
        
    def _set_timedrotatingfile_handler(logfile, base, time):
        try:
            handler_timedrotatingfile = logging.handlers.TimedRotatingFileHandler(
                logfile, when=base, interval=time, backupCount=0, encoding=None, 
                delay=False, utc=False)
            handler_timedrotatingfile.setFormatter(formatter)
            _add_log_handler(handler_timedrotatingfile)
        except IOError, e:
            if 'filename' in str(e):
                e = ("You may want to try escaping your logfile name with " + 
                     "an 'r' (raw). " + str(e))
                raise IOError(e)
            else:
                raise
        except Exception, e:
            raise
        
    def _set_mail_handler():
        e = "Will be implemented in a future release"
        raise NotImplementedError(e)
#             handler_mail = logging.handlers.SMTPHandler(
#                 mailhost, fromaddr, toaddrs, subject, credentials=None, 
#                 secure=None)
#             #333 Modify for error or above only 
#         .setFormatter(formatter)
#         _add_log_handler()
            
    def _set_memory_handler():
        e = "Will be implemented in a future release"
        raise NotImplementedError(e)
#             handler_memory = logging.handlers.BufferingHandler(capacity)
#         .setFormatter(formatter)
#         _add_log_handler()
                
    def _set_web_handler():
        e = "Will be implemented in a future release"
        raise NotImplementedError(e)
#             handler_web = logging.handlers.HTTPHandler(
#                 host, url, method='GET')            
#         .setFormatter(formatter)
#         _add_log_handler()
            
    def _set_socket_handler():
        e = "Will be implemented in a future release"
        raise NotImplementedError(e)
#             handler_socket = logging.handlers.SocketHandler(host, port)            
#         .setFormatter(formatter)
#         _add_log_handler()
                                
    def _set_dgram_handler():
        e = "Will be implemented in a future release"
        raise NotImplementedError(e)
#             handler_dgram = logging.handlers.DatagramHandler(host, port)            
#         .setFormatter(formatter)
#         _add_log_handler()
            
    def _add_log_handler(handle):
        self.vout.addHandler(handle)
        self.vlog.addHandler(handle)

    def _add_net_handler(handle):
        self.vnet.addHandler(handle)
                                            
    # Always set a screen handler
    # Checks that log level is an integer. 
    # If it fails, sets to default level of 40 (error)
    try:    loglevel = int(loglevel)
    except: log_level = 40

    ##################################             
    #Set the format for the log output
    formatter = logging.Formatter('%(asctime)s - ' + 
                                  '%(name)s - ' + 
                                  '%(levelname)s - ' + 
                                  '%(message)s')
    
    # create the different loggers
    self.vout   = logging.getLogger("vout." + str(app))
    self.vprint = logging.getLogger("vprint." + str(app))
    self.vlog   = logging.getLogger("vlog." + str(app))
    self.vnet   = logging.getLogger("vnet." + str(app))
    
    # Set the log handlers
    # Always set a screen handler, even if just for vprint
    _set_screen_handler()
    # Set the logfile if any exists
    if (
        (logfile is not None)                and 
        ("null" not in str(logfile).lower()) and 
        ("none" not in str(logfile).lower()) and 
        (str(logfile) != "") 
        ):
        logfile = re.sub('\s+', '', logfile)
        _set_logfile(logfile)
    else:
        _set_null_handler()
    # Set the logging level
    self.vout.setLevel(level=loglevel)
    self.vprint.setLevel(level=loglevel)
    self.vlog.setLevel(level=loglevel)
    self.vnet.setLevel(level=loglevel)

    return

def checkverbose(self):
    """ 
    """
    def _make_default_logger():
        # Default is null
        verbose(self, self.__class__.__name__, loglevel = 0)

    try:
        p = "^.+class.+logging.+Logger.+$"
        # Check vprint because it always exists in verbose logger
        # If the verbose logger is not correct, make a new one that logs null
        # If self.vprint does not exists, it goes to NameError
        # If it exists, but is not a class logging.Logger, recreate
        if not re.match(p, str(type(self.vprint))):
            # It is not the right thing, override
            _make_default_logger()
    except (NameError, AttributeError), e:
         _make_default_logger()

if __name__ == "__main__":
    class test(object):
        def __init__(self):
            pass
        
    o = test()
    o.test = "test"
    verbose(o, o.__class__.__name__, loglevel = 10, screen = True)
    o.vout.debug("this is a test")
    
    pass # Alwasy leave the pass