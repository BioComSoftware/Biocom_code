##############################################################################
# Removal of the "__license__" line or content from  "__license__", or removal
# of "__author__" in this or any constituent # component or file constitutes a
# violation of the licensing and copyright agreement.
__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = "Telemend"
__license_file__= "Clause1.PERPETUAL_AND_UNLIMITED_LICENSING_TO_THE_CLIENT.py"
__version__     = "0.9.6.0"
__maintainer__  = "Mike Rightmire"
__email__       = "Mike.Rightmire@BiocomSoftware.com"
__status__      = "Development"
##############################################################################


from BiocomCommon.loghandler import log
from BiocomCommon.errorhandler.formatters import _format_original_error,_log_error
from BiocomCommon import move_file
from BiocomCommon.errorhandler.customexceptions import CustomError,FatalException
from BiocomCommon import checks
from datetime import datetime

import re
import shutil
import subprocess
import sys
import os

### SPECIFIC ERROR HANDLERS
# These functions perform specific actions on the 'self' object These are used
# to handle errors and return to the lone below the error call, UNLESS the
# a new fatal exception is raised, which will halt all scripts.
# The keyword 'fatal' in the error message passed to errorhandler will raise a
# fatal exception and halt the scripts.

# ErrorHandler calls the proper handler method from here based on the error
# keyword matched in the error string passed to the ErrorHandler.
#
# The search is done as...
#  if str(MethodName).lower() in str(error_string).lower():
#
# The error keyword MUST MATCH THE METHOD NAME
#
# NOTE:
#       THIS MEANS if you have two methods, 'ERR1' AND 'ERR10',
#       'ERR1' will always be the one found...SO IT IS RECOMMENDED YOU NAME
#       THE METHODS VERY UNIQUELY AND CAREFULLY.
#       I.e. 'StringNotFoundInLogError'
class Handlers(object):
    """
    :USAGE:
        =========================================================
        Currently, these handlers only work within class objects.
        =========================================================
    
        STEP ONE: The @handlertry decorator must be added to the main 
                  body of the code to be handled. 
                  
        The @handlertry system can be used in code in three ways:

        1.  In this form , the 'TriggerMessage' handles the entire method. 
            In this case, any error will be handled by the handlertry, and 
            there is no need for an additional try/except. 
        <myclass>
            @handlertry("TriggerMessage: ", tries = 2)
            def myMethod(self, args, kwargs):
                FH = open(filename, "w+", 0)
                return FH

            Some more code here (After handling, control always returns here, 
                                  unless a controlled program end is called.)
                                  
        2. In this form, the @handlertry is left generic, and the TriggerMessage 
           is passed through the error message. In this case, a try/except 
           must be included to add the TriggerMessage to the error. 
           
           @handlertry("")
            def myMethod(self, args, kwargs)::    
                try:
                    FH = open(filename, "w+", 0)
                    return FH
                except (Exception, Exception) as e:
                    e.message = ('TriggerMessage: ' + e.message)
                    raise type(e)(e.message)

            Some more code here (After handling, control always returns here, 
                                  unless a controlled program end is called.)

        3. Use a generic @handlertry, and simply call an exception with 
           the TriggerMessage as the entire custom message. 

           @handlertry("")
            def myMethod(self, args, kwargs)::    
                if a == b:
                    <perform code>
                else:
                    raise Exception('TriggerMessage')

            Some more code here (After handling, control always returns here, 
                                  unless a controlled program end is called.)
           
           
        STEP TWO: Create the individual handlers. See the 'Template' method
                  for details on how to do this. 
                  
        ------------------------
        The above results in ...
        ------------------------

    1. Attempting to run the line of code 'FH = open("invalidfilename, "r+", 0)'

    2. Upon failure, control is passed to ErrorHandler.customErr()

    3. Based on the "InvalidFileName" in the message, control is passed to
       ErrorHandler.InvalidFileName(). 

    4a.If the InvalidFileName handler can correct the issue, control is passed 
       back to the calling script, at the line FOLLOWING the completion of the 
       originally decorated method and code continues to run.
       
    4b.If the InvalidFileName handler CANNOT correct the issue, it can continue 
       to try and fix the issue, and re-run the decorated method, for "tries" 
       number of attempts...until success or control is passed back to the line 
       following the decorated method.                    
    """

# IGNORE ALL ERRORS ABOUT PUTTING 'self' AS FIRST PRAMATER
    
    def TEMPLATE(callobj, tries, args, kwargs, e, GETMEMBERS, STACK):
        """
        :NAME:
            template(callobj, args, kwargs, e)
            
        :DESCRIPTION:
        ===========================================================================
        A HANDLER METHOD MUST RETURN: 
            args, kwargs, <Some result, be it True/False/str/whatever>
        ===========================================================================
        
            This is a template for special error handlers to be used by 
            ErrorHandler when called by the handlertry decorator. It both parses 
            the information to be passed to the callobj log, as well as controls 
            attempts to fix the problem.
            
            The method name "TEMPLATE" should be replaced with a human-readable
            name WHICH MATCHES the trigger phrase used in handlertry AND 
            matches the search line in the custom Error string (see usage).  
            
            =================================================================
            'ErrorHandler' calls the proper handler method based on the error 
            keyword matched in the error string passed to the ErrorHandler. 
            =================================================================
            
            The search is done as...
             if str(MethodName).lower() in str(error_string).lower():
            
            The error keyword MUST MATCH THE METHOD NAME. I.e. To match 'TEMPLATE'
            the error string would have to be something like ...
            'Error: TEMPLATE Your thing in line 222 didn't work'
            
            THIS MEANS if you have two methods, 'ERR1' AND 'ERR10', the following...
            'Error: ERR1 Your thing in line 222 didn't work'
            'Error: ERR10 Your thing in line 222 didn't work'
            
            ... will always match method ERR1 ...SO IT IS RECOMMENDED YOU NAME
            THE METHODS VERY UNIQUELY AND CAREFULLY.
            
            I.e. 'StringNotFoundInLogError' 
            
        ===========================================================================
        A HANDLER METHOD MUST RETURN: 
            args, kwargs, <Some result, be it True/False/str/whatever>
        
        The following error is often indicative of the return being incorrect...
        
        Traceback (most recent call last):
             File "test.py", line xx, in <module>
             object.method('arg1', 'arg2', kwarg1=1, kwarg2=2)
             File "/opt/lib/errorhandler/trywrappers.py",line 218,in wrapped
             stack()
             TypeError: 'NoneType' object is not iterable
        ===========================================================================
            
               
        :ARGUMENTS:
            self:    The ErrorHandler class object (standard use of self).  
    
            callobj: The "self" class object that used the handlertry decorator
                     which, in turn, resulted in the call of this method. The 
                     handler method can then act directly on this object during it's 
                     attempts to correct the problem.  
                     
            args:    The "args" of the method decorated by handlertry. These
                     can be modified and passed back to the decorated method
                     for its attempts to re-run the method.
                     
            kwargs:  The "kwargs" of the method decorated by handlertry. These
                     can be modified and passed back to the decorated method
                     for its attempts to re-run the method.
                     
            e:       The original error raised by the method decorated by 
                     handlertry. I.e. when the decorator trywrappers.handlertry
                     run the function, it grabs excetions as follows:
                     
                     try:
                         <code>
                     except Exception as e:
                         <e passed here>>
        
        :VARIABLES:
            No userland variables. 
            
        :RETURNS:
            args:    The original passed in parameter 'args', AFTER any 
                     modifications performed by this method.  
            
            kwargs:  The original passed in parameter 'kwargs', AFTER any 
                     modifications performed by this method.  
            
            result:  Any result to be passed back to the original decorated 
                     object method which raised the original error as 'e'.
        
        ===========================================================================
        A HANDLER METHOD MUST RETURN: 
            args, kwargs, <Some result, be it True/False/str/whatever>
        
        The following error is often indicative of the return being incorrect...
        
        Traceback (most recent call last):
             File "test.py", line xx, in <module>
             object.method('arg1', 'arg2', kwarg1=1, kwarg2=2)
             File "/opt/lib/errorhandler/trywrappers.py",line 218,in wrapped
             stack()
             TypeError: 'NoneType' object is not iterable
        ===========================================================================
                     
    
        :USAGE:
            <the following lines added to customErr above>
            elif 'TriggerPhrase' in str(e): 
                return self.TriggerPhrase(callobj, args, kwargs, e)
            
            def TriggerPhrase(callobj, args, kwargs, e):
                # Messages and corrective code placed in appropriate places here
                return args, kwargs, final,  result
        """
        print 'In TEMPLATE' #3333
        final = False
        # Create custom message to BE SENT TO THE LOGGER
        message = ("".join(["Template message part 1 is a list item. ", 
                            "Template message part 2 is a list item."]))    

        # Sends the message and original error to the LOGGER
        # Remove this line if you don't want an error displayed
        _log_error(message, e)
        ### METHOD ACTIONS
        # CODE BELOW TO CORRECT ISSUE
        # All code should act on the 'callobj' object
        
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # MUST RETURN: args, kwargs, <Some result, be it True/False/str/whatever>
        #
        #The following error is often indicative of the return being incorrect
        #
        # Traceback (most recent call last):
        #     File "test.py", line xx, in <module>
        #     object.method('arg1', 'arg2', kwarg1=1, kwarg2=2)
        #     File "./errorhandler/trywrappers.py", line 218, in wrapped
        #     stack()
        #     TypeError: 'NoneType' object is not iterable
    
#         return args, kwargs, final,  True
        return args, kwargs, final,  str(sys._getframe().f_code.co_name)

    def ConfigFileNotFound(callobj, tries, args, kwargs, e, GETMEMBERS, STACK):
        """"""
        final = False
        # Create custom message to BE SENT TO THE LOGGER
        message = ("".join(["The configuration file was not found. ",
                            "Please verify the file exists in the ",
                            "appropriate path and is readable."]))
        # Sends the message and original error to the LOGGER
        # Remove this line if you don't want an error displayed
        _log_error(message, e)
        ### METHOD ACTIONS
        # CODE BELOW TO CORRECT ISSUE
        # All code acts on the self object
        raise FatalException()

    def CannotOpenSQLAlchemyConnection(callobj, tries, args, kwargs, e, GETMEMBERS, STACK):
        """"""
        final = False
        # Create custom message to BE SENT TO THE LOGGER
        message = ("".join([]))
        # Sends the message and original error to the LOGGER
        # Remove this line if you don't want an error displayed
        _log_error(message, e)
        ### METHOD ACTIONS
        # CODE BELOW TO CORRECT ISSUE
        # All code acts on the self object
        print 'In CannotOpenSQLAlchemyConnection'
        print 'args:', args #333
        print 'kwargs:', kwargs #3333
        return args, kwargs, final,  True

    def ConfigFileNoOption(callobj, tries, args, kwargs, e, GETMEMBERS, STACK):
        """"""
        final = False
        # Create custom message to BE SENT TO THE LOGGER
        message = ("".join(["Unable to find the specified section or option",
                            "(variable) in config file. ",
                            "Please verify the contents of the file. "]))
        # Sends the message and original error to the LOGGER
        # Remove this line if you don't want an error displayed
        _log_error(message, e)
        ### METHOD ACTIONS
        # CODE BELOW TO CORRECT ISSUE
        # All code acts on the self object
        return args, kwargs, final,  None

    def ConfigFileParseError(callobj, tries, args, kwargs, e, GETMEMBERS, STACK):
        final = False
        # Create custom message to BE SENT TO THE LOGGER
        message = ("".join(["The configuration file contains errors. ",
                            "Please verify the contents of the file. "]))
        # Sends the message and original error to the LOGGER
        # Remove this line if you don't want an error displayed
        _log_error(message, e)
        ### METHOD ACTIONS
        # CODE BELOW TO CORRECT ISSUE
        # All code acts on the self object
        raise FatalException()

    def PassThroughException(callobj, tries, args, kwargs, e, GETMEMBERS, STACK):
        final = False
        # Custom message to BE SENT TO THE LOGGER
        message = ("")
        # Sends the message and original error to the LOGGER
        _log_error(message, e)
        ### METHOD ACTIONS
        return args, kwargs, final,  None

    def DBHandlerInvalidHostname(callobj, tries, args, kwargs, e, GETMEMBERS, STACK):
        final = False
        # Custom message to BE SENT TO THE LOGGER
        print 'args=', args#3333
#         print 'len(args)=', len(args) #333
#         print 'args[0]=', args[0]#3333
        print 'kwargs=', kwargs#3333
        message = ''.join(["'DBHandler.host'(", str(args[0]), ") does not appear to be in a proper format."])
        args = list(args)
        print message
        args[0] = raw_input('Please re-enter the server name or IP address...')
        args = tuple(args)
        # Sends the message and original error to the LOGGER
        _log_error(message, e)
        ### METHOD ACTIONS
        if tries >= 1: final = True
        return args, kwargs, final, None

#     @classmethod
#     def UnknownException(*args, **kwargs):

    def UnknownException(callobj, tries, args, kwargs, e, GETMEMBERS, STACK):
        """"""
        print 'IN UnknownException' #3333
        final = False
        callobj = kwargs.pop('callobj', None)
        e       = kwargs.pop('e', '')

        # Custom message to BE SENT TO THE LOGGER
        message = ("".join([
                            "An unidentified exception was passed. ",
                            "'errorhandler' does not know what to do. ",
                            "Calling fatal exception and halting. (",
                            str(e), "). "
                            ]))
        # Sends the message and original error to the LOGGER
        _log_error(message, e)
        ### METHOD ACTIONS
#         raise FatalException(e) # Does not return
        return args, kwargs, final,  None
  
  # FOR UNITTEST  


if __name__ == '__main__':
    import inspect
    from BiocomCommon.loghandler import log
    
    log.error("Starting handlers unittest. Ignore errors from 'handlers_unittest_ignore_me'", 
                app_name   = 'handlers_unittest_ignore_me',
                logfile    = 'system',
                log_level  = 10,
                screendump = False
                 )
    
    class test():
        def __init__(self):
            pass

    # Set 'e'
    try:
        this_error_was_passed_in_to_handler
    except Exception as pass_in_err:
        pass

    callobj = test()
    args = ('a', 0)
    kwargs = {'kwargument_text':'Test argument', 'kwargument_num':1}

    members = inspect.getmembers(Handlers, predicate=inspect.ismethod)
    for i in members:
        output = str(i[0]) + ':'
        if 'UnknownException' not in str(i[0]):
            try:
                result = Handlers.__dict__[i[0]](callobj, args, kwargs, pass_in_err)
                output = output + str(result)
            except Exception as e: # any exception
                output = output + "(RAISED ERROR '" + str(e) + "')"
            print output
    print 'OK'

