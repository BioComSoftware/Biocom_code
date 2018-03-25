##############################################################################
# Removal of the "__license__" line or content from  "__license__", or removal 
# of "__author__" in this or any constituent # component or file constitutes a 
# violation of the licensing and copyright agreement. 
__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = "PERPETUAL_AND_UNLIMITED_LICENSING_TO_THE_CLIENT"
__license_file__= "Clause1.PERPETUAL_AND_UNLIMITED_LICENSING_TO_THE_CLIENT.py"
__version__     = "0.9.6.0"
__maintainer__  = "Mike Rightmire"
__email__       = "Mike.Rightmire@BiocomSoftware.com"
__status__      = "Development"
##############################################################################

import inspect

import re

class CustomError(Exception):
    """
    Base user extensible exception class
    Baseclass for dealing with unhandled errors
    Extends class Exception
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class FatalException(CustomError):
    """
    raise FatalSocketError
    Returns default error + the attached string message
    "Socket encountered a fatal condition. "
    
    EVENTUALLY this needs to cleanly close out the current processes, and 
    return the user to the start GUI. For now, it creates program halt.   
    """
    def __init__(self, message = None):
        self.message = ("")
        CustomError.__init__(self, self.message)

#err = ''.join([self.__class__.__name__, ".", inspect.stack()[0][3], ": ", "The '@property' path value '", value, "' does not appear to exist or is not readable." ])


class PropertyNotSetError(Exception):
    """
    :NAME:
        PropertyNotSetError(message, [USAGE = String])
    
    :DESCRIPTION:
        PropertyNotSetError is a custom error message to use with @property 
        decorated class attributes, to be raised when the variable is accessed
        prior to having been set with the @variablename.setter. 
        
    :PARAMETERS:
        message:     Can be a normal error message, or simply the name of the 
                     property variable that was not set. 
                     
                     If a single word is passed in, it is assumed to be a 
                     property name, and an error message is created referencing
                     the property name. If it is a complex string, the entire
                     message is raised as normal. 
                      
        USAGE:       Is an optional parameter to include the expected value/type
                     for the parameter. It is just a string, and will be added
                     to the end of the message. 
                     
    :USAGE:
        @property
        def var(self):
            try: 
                return self.VAR
            except (AttributeError, NameError, KeyError) as e:
                raise PropertyNotSetError(
                        'var', # The name of this method (var)
                        USAGE = "'var' must be a list])
                        )
    """
    def __init__(self, message, USAGE = ''):
        message = str(message)
        USAGE = str(USAGE)
#         callingclass = str(stack()[0][0].f_locals["self"].__class__)
        # If 'message' is a single word, assume it is the property (this is the proper usage)
        if re.match(r'\A[\w-]+\Z', message):
                    newmessage = "The @property '{P}' has not yet been set. ".format(P=message)
                    # Add the USAGE param if applicable
                    if len(USAGE) > 0: newmessage += USAGE
                    
        else:
            # A fuller string has been passed in. So just pass it along. 
            newmessage = message 
            if len(USAGE) > 0: newmessage += " " + str(USAGE)
        # Now call the parent __init__ which raises error
        super(PropertyNotSetError, self).__init__(newmessage)


class PropertyNotValidValueError(Exception):
    """
    :NAME:
        PropertyNotValidValueError(message, [USAGE = String])
    
    :DESCRIPTION:
        PropertyNotValidValueError: a custom error message to use with @property 
        decorated class attributes, to be raised when an attemot is made to 
        set a @property variable with imporper or unexpected 
        contents (via variablename.setter). 
        
    :PARAMETERS:
        message:     Can be a normal error message, or simply the name of the 
                     property variable that was not set. 
                     
                     If a single word is passed in, it is assumed to be a 
                     property name, and an error message is created referencing
                     the property name. If it is a complex string, the entire
                     message is raised as normal. 
                      
        USAGE:       Is an optional parameter to include the expected value/type
                     for the parameter. It is just a string, and will be added
                     to the end of the message. 
                     
    :USAGE:
        @property
        def var(self):
            try: 
                return self.VAR
            except (AttributeError, NameError, KeyError) as e:
                raise PropertyNotSetError(
                        'var', # The name of this method (var)
                        USAGE = "'var' must be a list])
                        )
    """
    def __init__(self, message, value = None, valid = None, USAGE = None):
        """"""
#         callingclass = str(stack()[0][0].f_locals["self"].__class__)
        # If 'message' is a single word, assume it is the value (this is the proper usage)
        if re.match(r'\A[\w-]+\Z', message):
            newmessage = "The value passed for @property '{P}' does not appear to be of a valid type or content. ".format(P=message)
        else:
            newmessage = message

        if valid is not None: 
            newmessage += "(valid type = '{V}'). ".format(V = str(valid))
        
        if value is not None: 
            newmessage += "(value = ({T})'{V}'). ".format(V = str(value), T = str(type(value)))
        
        if USAGE is not None: 
            newmessage += str(USAGE)
                    
        # Now call the parent __init__ which raises error
        super(PropertyNotValidValueError, self).__init__(newmessage)


class PropertyCannotBeSetError(Exception):
    """
    :NAME:
        PropertyCannotBeSetError(message, [USAGE = String])
    
    :DESCRIPTION:
        PropertyCannotBeSetError:  
        
    :PARAMETERS:
        message:     Can be a normal error message, or simply the name of the 
                     property variable that was not set. 
                     
                     If a single word is passed in, it is assumed to be a 
                     property name, and an error message is created referencing
                     the property name. If it is a complex string, the entire
                     message is raised as normal. 
                      
        USAGE:       Is an optional parameter to include the expected value/type
                     for the parameter. It is just a string, and will be added
                     to the end of the message. 
                     
    :USAGE:
        @property
    """
    def __init__(self, message, value = None, USAGE = ''):
        """"""
#         callingclass = str(stack()[0][0].f_locals["self"].__class__)
        # If 'message' is a single word, assume it is the propert (this is the proper usage)
        if re.match(r'\A[\w-]+\Z', message):
            newmessage = "The @property '{P}' (type:{T}) cannot be set manually.".format(P=message, T=type(message))
            if value is not None: newmessage += "(value: '{V}'). ".format(V = str(value))
            # Add the USAGE param if applicable
            if len(USAGE) > 0: newmessage += USAGE
                    
        else:
            # A fuller string has been passed in. So just pass it along. 
            newmessage = message
            if len(USAGE) > 0: newmessage += " " + str(USAGE)
        # Now call the parent __init__ which raises error
        super(PropertyCannotBeSetError, self).__init__(newmessage)



class RegressionTest(object):
    def __init__(self, error, USAGE = 'USAGE message here...'):
        if   error == 'PropertyNotSetError': raise PropertyNotSetError(inspect.stack()[0][3], USAGE = USAGE)
        elif error == 'PropertyNotValidValueError': raise PropertyNotValidValueError(inspect.stack()[0][3], USAGE = USAGE)
        elif error == 'FatalException': raise FatalException(inspect.stack()[0][3])
        else:
            err = "Error class '{E}' does not exist. ".format(E = str(error))
            raise Exception(err)
        
if __name__ == '__main__':
    RegressionTest("PropertyNotSetError")
#         raise PropertyNotSetError('test', USAGE = "USAGE")
#         raise PropertyNotValidValueError(inspect.stack()[0][3], USAGE = "USAGE")
