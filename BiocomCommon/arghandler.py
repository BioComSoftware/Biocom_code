##############################################################################
# Removal of the "__license__" line or content from  "__license__", or removal 
# of "__author__" in this or any constituent # component or file constitutes a 
# violation of the licensing and copyright agreement. 
__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = ""
__license_file__= "Clause1.PERPETUAL_AND_UNLIMITED_LICENSING_TO_THE_CLIENT.py"
__version__     = "0.9.1.0"
__maintainer__  = "Mike Rightmire"
__email__       = "Mike.Rightmire@BiocomSoftware.com"
__status__      = "Development"
##############################################################################
# from qrnote.errorhandler   import handlertry
# from qrnote.errorhandler   import raisetry

from BiocomCommon.checks import Checks
checks = Checks()
_slash = checks.directory_delimiter() 

def override_kw_vars(self, kwargs):
    for key in kwargs.keys():
        self.config.__dict__[key] =  kwargs[key]
    return True

def set_mandatory_defaults(self, _dict):
    """
    In the event the config file does not have the mandatory variables,
    and they are not passed in as __init__ variables, they can be set here.
    These defaults can be modified. The order of setting defaults should be:
    1. config file
    2. __init__ parameters
    3. Here (_set_mandatory_defaults)
    """
    for key in _dict.keys():
        if key not in self.config.__dict__.keys():
            self.config.__dict__[key] = _dict[key]
    return

def iterate_argv_flags(argv):
    """
    Must always be an argv from Python command line
    
    Splits out the 'flags' from the 'flag = something"s
    
    Yields flags as iterator
    """
    (flags, kwargs) = separate_argv(argv)
    for flag in flags: yield flag  

def iterate_argv_kwargs(argv):
    """
    Must always be an argv from Python command line
    
    Splits out the 'flags' from the 'flag = something"s
    
    Yields flags as iterator
    """
    (flags, kwargs) = separate_argv(argv)
    for key, value in kwargs.iteritems():
        yield key, value

def separate_argv(argv):
    """
    Must always be an argv from Python command line
    
    Splits out the 'flags' from the 'flag = something"s
    """
    def _clean_key(value):
        return value.lstrip('-') # remove all leading '-'
        

#     print 'argv=', argv #333        
    # First is always the filename
    filename = argv.pop(0)
    if not filename.endswith('.py'):
        err = "arghandler.separate_argv: Does not appear to be a valid sys.argv list. First item '{P}' is not a valid file path. ".format(P = filename)
        raise ValueError(err)
#     print 'argv=', argv #333        

    args = []
    kwargs = {}
    key = None # Set initial. This cycles as a flag also
    for arg in argv: # whats left
#         print 'arg: ', arg
        if not arg.startswith("-"): # value indicator
#             print 'It doesnt start with -'
            if key:
                kwargs[key] = arg # Add to kwargs
                key = None # reset
            elif key is None: # different from empty
                key = _clean_key(arg)
            else: # Key not set. If we have an arg value but no key, somethings wrong
                err = "arghandler.separate_argv: The value of '{V}' was found in argv, but no proper preceding key has been found. ".format(V = str(arg))
                raise ValueError(err)

        else: # Started with '-'
#             print 'It DOES start with -'
            if key: # Has a preceding proper key
#                 print 'key already =', key
                args.append(key)
#             print "_clean_key(arg)=", _clean_key(arg) #333
            key = _clean_key(arg)
    # If we're done, and there's still a key value, then its a flag
    if key: 
        args.append(key) 
    
    return args, kwargs


        
if __name__ == '__main__':
    import sys
    print sys.argv
    print separate_argv(sys.argv)
            
         