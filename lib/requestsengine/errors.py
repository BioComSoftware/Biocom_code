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


import sys

class customerror(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)
    
class FormNotSelected(customerror):
    """
    raise FormNotSelected
    Returns default error + the attached string message
    "Form does not appear to have been selected within browser object. Please 
     use '<scraper>.setform(Formname)' to set the form."

    All attempts to perform form actions before the form has been set will 
    fail. 
    """
    def __init__(self, message = None):
        self.message = ("Form does not appear to have been selected " + 
                        "within browser object. Please use " + 
                        "'<scraper>.setform(Formname)' to set the form." + 
                        "[Original error: " + str(message) + "]")
        customerror.__init__(self, self.message)
    
class URLNotSelected(customerror):
    """
    raise URLNotSelected
    Returns default error + the attached string message
    "The URL, site or page does not appear to have been selected within browser 
    object. Please use '<scraper>.setpage(URL)' to set the site."

    All attempts to perform browser actions before the site has been set will 
    fail. 
    """
    def __init__(self, message = None):
        self.message = ""
        customerror.__init__(self, self.message)
    
class URLNotFormatted(customerror):
    """
    raise URLNotFormatted
    Returns default error + the attached string message
    "URL does not meet the format 'http(s)://server.dom' or 
    'http(s)://name.server.dom'. Please reformat your input."
    """
    def __init__(self, message = None):
        self.message = ("URL does not meet the format " + 
                        "'http(s)://server.dom' or 'http(s)://name.server.dom'" + 
                        "\n Please reformat your input.\n" + 
                        "[Original error: " + str(message) + "]")
        customerror.__init__(self, self.message)

class errors:
    """
    NAME
        error
    
    FILE
        errors.py
    
    DESCRIPTION
        Used for generating both custom unhandled exceptions, and 
        for handling exceptions with specific actions. 
        
        An existing class object MUST be passed in. Attributes within this 
        object can be referenced by "caller". I.e. caller.var = 10
        
        Uses the self.log() parameter of an EXISTING instantiated class object
        to generate output. If a  logger has not been instantiated in the 
        calling object, a default one will be generated pushing info to screen.

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
        
    USER EXCEPTION CLASSES
        UnknownError(customerror):
    """
    def __init__(self, caller):
        self.caller = caller

    def _format_original_error(self, e):
        return str("[Original error: " + str(e) + "]")
    
    def _custom_error(self, message, e):
        # Format message
        e = message + str(self._format_original_error(e))
        # Send to log
        self.caller.vout.error(e)
        return
        
    def handle(self, e):
        # Server socket port is already in use
        if "URLNotSelected"  in str(e):self.URLNotSelected(e)
        if "URLNotFormatted" in str(e):self.URLNotFormatted(e)
        # elif: # More error checks here
        else:
            message = ("An unhandled or unknown exception was received." + 
                       "Method 'error.handle()' does not know what to do " + 
                       "with this error. logging and continuing...")
            self._custom_error(message, e)
                
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

    def AuthenticationError(self, e):
        message = ("The attempted send failed with an authentication error. " + 
                   "Please check your SID and Token. Continuing to listen. ")
        self._custom_error(message, e)
        ### ACTION
        # No action needed. Logging only
        sys.exit(0)

    def URLNotFormatted(self, e):
        # custom message to BE SENT TO THE LOGGER
        message = ("URL appears to be incorrectly formatted. ")
        # Sends the message and original error to the LOGGER
        #Remove this line if you don't want an error displayed
        self._custom_error(message, e)
        ### METHOD ACTIONS
        # No action 
        sys.exit(0)
        
    def URLNotSelected(self, e):
        message = ("The URL, site or page does not appear to have been " + 
                    "selected within browser object. Please use " + 
                    "'<scraper>.setpage(URL)' to set the site.\n" + 
                    "[Original error: " + str(e) + "]")
        self._custom_error(message, e)
        ### ACTION
        # No action 
        sys.exit(0)
        
    def UnverifiedSourceNumber(self, e):
        # Custom message to BE SENT TO THE LOGGER
        message = ("Twilio refused send due to unverified phone number.")
        # Sends the message and original error to the LOGGER
        self._custom_error(message, e)
        ### METHOD ACTIONS
        # None