#!/usr/bin/python

##############################################################################
# Removal of the "__license__" or "Freelancer_Perpetual_License.py" from 
# "__license__", or removal of "__author__" in this or any constituent 
# component or file constitutes a violation of the licensing and copyright 
# agreement.
__author__      = "Mike Rightmire"
__copyright__   = ""
__license__     = "Freelancer_Perpetual_License.py"
__version__     = "0.9.0.0"
__maintainer__  = ""
__email__       = ""
__status__      = "Beta"
##############################################################################

import sys

### Baseclass for dealing with unhandled errors
#   Extends class Exception
class customerror(Exception):
    """
    Base user extensible exception class
    """
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

### Specific classes for dealing with unhandled exceptions
#   Extends class customerror    
class UnknownFatalError(customerror):
    """
    raise UnknownFatalError('message')
    """
    def __init__(self, message = None):
        self.message = ("An unknown fatal error was raised" + 
                        "[Original error: " + str(message) + "]")
        customerror.__init__(self, self.message)

######
# MAIN
class error:
    """
    NAME
        error
    
    FILE
        custom_errors.py
    
    DESCRIPTION
        Used for generating both custom unhandled exceptions, and 
        for handling exceptions with specific actions. 
        
        An existing class object MUST be passed in
        Uses the self.log() parameter of an EXISTING instantiated class object
        to generate output. A logger has to be instantiated in the calling class
        objject for this class to be used.

    EXAMPLE
        import custom_errors
        class CallingClass(object):
        def __init__(self, log_level = 40, logfile = None):
            self.log = create_logger(self, logfile, log_level)        
            self.error = custom_errors.error(self)
        try:
            print this wont work
        except:
            self.error.handle(e)

    CLASS self()
        METHODS
            _format_original_error(self, e)
            
            _custom_error(self, message, e)
            
            handle(self, e)
                Error message handler. Generates logfile output
            
            TEMPLATE(self, e)
                Create custom error message, exceptions, and code to run
                to handle exceptions
                
    USER ERROR METHODS
        PortInUse(e)
        AuthenticationError(e)
        
    USER EXCEPTION CLASSES
        FatalTwiliosockError(customerror):
        UnknownTwiliosockError(customerror):
        FatalThreadError(customerror):
        UnknownThreadError(customerror):
        FatalSocketError(customerror):
        UnknownSocketError(customerror):
        UnknownError(customerror):
    """
    def __init__(self, callerobj):
        self.callerobj = callerobj

    def _format_original_error(self, e):
        return str("[Original error: " + str(e) + "]")
    
    def _custom_error(self, message, e):
        # Format message
        e = message + str(self._format_original_error(e))
        # SSend to log
        self.callerobj.log.error(e)
        return
        
    def handle(self, e, source, frame):
        
        errorin = str(source[6][1])
        errorin = errorin.replace("implementedBy", "")
        errorin = "".join(c for c in errorin if c not in "<>")
        errorin = errorin + "." + str(frame[0][3])
        errorin = errorin + "(line:" + str(frame[0][2]) + "): "
        
        e = errorin + str(e)
                
        #ERRORS
        if  ("fatal") in str(e).lower()             :self.UnknownFatalError(e)
        elif ("InvalidFilePath") in str(e).lower()  :self.InvalidFilePath(e)
        elif ("InvalidWebDriver") in str(e).lower() :self.InvalidWebDriver(e)
        elif ("IncorrectPage") in str(e).lower()    :self.IncorrectPage(e)
        elif ("Cannotloadelement") in str(e).lower():self.Cannotloadelement(e)
        elif ("CannotSendKeys") in str(e).lower()   :self.CannotSendKeys(e)
        elif ("NotYetImplemented")in str(e).lower() :self.NotYetImplemented(e)
        # elif: # More error checks here

        else: self.UnknownFatalError(e)
                
    ### SPECIFIC ERROR HANDLERS 
    # These functions perform specific actions on the 'self' object and 
    # return the object. These are used to handle errors and kick the object 
    # back into play
############################    
#     def TEMPLATE(self, e):
#         # Create custom message to BE SENT TO THE LOGGER
#         message = ("Error message")
#         # Sends the message and original error to the LOGGER
#         #Remove this line if you don't want an error displayed
#         self._custom_error(message, e)
#         ### METHOD ACTIONS
#         # Put the code here to actually handle the error
#         # "Handling it" can also be defined as just raising one
#         # of the Error classes above
#         ## raise FatalSocketError()
#         sys.exit(0)
############################

    def Cannotloadelement(self, e):
        # custom message to BE SENT TO THE LOGGER
        message = ("A searched-for element on the page cannot be found. ")
        # Sends the message and original error to the LOGGER
        #Remove this line if you don't want an error displayed
        self._custom_error(message, e)
        ### METHOD ACTIONS
        # Put the code here to actually handle the error
        # "Handling it" can also be defined as just raising one
        # of the Error classes above
        ## raise FatalSocketError()
        # None
    
    def CannotSendKeys(self, e):
        # custom message to BE SENT TO THE LOGGER
        message = ("Unable to send 'element.sendkeys(<text>) to the " + 
                   "selected element. ")
        # Sends the message and original error to the LOGGER
        #Remove this line if you don't want an error displayed
        self._custom_error(message, e)
        ### METHOD ACTIONS
        # Put the code here to actually handle the error
        # "Handling it" can also be defined as just raising one
        # of the Error classes above
        ## raise FatalSocketError()
        # None
                      
    def IncorrectPage(self, e):
        # custom message to BE SENT TO THE LOGGER
        message = ("The page does not appear to be the requested page of: " + 
                   str(self.URL))
        # Sends the message and original error to the LOGGER
        #Remove this line if you don't want an error displayed
        self._custom_error(message, e)
        ### METHOD ACTIONS
        # Put the code here to actually handle the error
        # "Handling it" can also be defined as just raising one
        # of the Error classes above
        ## raise FatalSocketError()
        # None
                
    def InvalidFilePath(self, e):        
        # custom message to BE SENT TO THE LOGGER
        message = ("The path given does not appear to be valid.")
        # Sends the message and original error to the LOGGER
        #Remove this line if you don't want an error displayed
        self._custom_error(message, e)
        ### METHOD ACTIONS
        # Put the code here to actually handle the error
        # "Handling it" can also be defined as just raising one
        # of the Error classes above
        ## raise FatalSocketError()
        # None
        
    def InvalidURL(self, e):
        # custom message to BE SENT TO THE LOGGER
        message = ("URL appears to be incorrectly formatted. ")
        # Sends the message and original error to the LOGGER
        #Remove this line if you don't want an error displayed
        self._custom_error(message, e)
        ### METHOD ACTIONS
        # Put the code here to actually handle the error
        # "Handling it" can also be defined as just raising one
        # of the Error classes above
        ## raise FatalSocketError()
        # None
        
    def InvalidWebDriver(self, e):
        # custom message to BE SENT TO THE LOGGER
        message = ("TThe WebDriver selected appears to be invalid. ")
        # Sends the message and original error to the LOGGER
        #Remove this line if you don't want an error displayed
        self._custom_error(message, e)
        ### METHOD ACTIONS
        # Put the code here to actually handle the error
        # "Handling it" can also be defined as just raising one
        # of the Error classes above
        ## raise FatalSocketError()
        # None

    def NotYetImplemented(selfself, e):
        # custom message to BE SENT TO THE LOGGER
        message = ("")
        # Sends the message and original error to the LOGGER
        #Remove this line if you don't want an error displayed
        self._custom_error(message, e)
        ### METHOD ACTIONS        

    def UnknownFatalError(self, e):
        message = ("")
        self._custom_error(message, e)
        ### ACTION
        # sys.exit(0) simply halts this attempt to open a new twiliosock 
        # object instance, however existing objects using with this port will 
        # still be functional.
        raise UnknownFatalError(e)
        