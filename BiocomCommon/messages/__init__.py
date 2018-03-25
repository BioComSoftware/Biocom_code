##############################################################################
# Removal of the "__license__" line or content from  "__license__", or removal
# of "__author__" in this or any constituent # component or file constitutes a
# violation of the licensing and copyright agreement.
__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = "Telemend"
__license_file__= "Clause1.PERPETUAL_AND_UNLIMITED_LICENSING_TO_THE_CLIENT.py"
__version__     = "0.9.7.0"
__maintainer__  = "Mike Rightmire"
__email__       = "Mike.Rightmire@BiocomSoftware.com"
__status__      = "Development"
##############################################################################

from ConfigParser import SafeConfigParser
import inspect
import ntpath

class MESSAGE(object):
    """
    """    
#     __exists = False
    
    def __new__(cls, key, *args, **kwargs):
        
        key = str(key).lower()

        if not hasattr(cls, 'instance'):
            # Create instance            
            cls.instance = super(MESSAGE, cls).__new__(cls)
            print 'if cls.instance=', cls.instance #3333
                    

            _path = inspect.getfile(cls.instance.__class__)
            print '_path=', _path #333
            _path, file = ntpath.split(_path)              
            print '_path=', _path #333
            config = SafeConfigParser()
            print 'config=', config #3333
            _file = _path + '/messages.conf'
            print '_file=', _file #333
            config.read(_file)
      
            for section in config.sections():
                # Check for specific section, otherwise assume table
                options = config.options(section)
                for option in options:
                    print 'option=', option #3333
                    cls.instance.__dict__[option] = str(config.get(section, option)) 

            result = ''.join([cls.instance.__dict__[key], "(args: ", str(args), ", kwargs: ", str(kwargs), "). "]) 
#             
            return result

        else:
            print 'else cls.instance=', cls.instance #3333
            
#             cls.instance.__exists = True
#             print 'MESSAGES object already exists' #333
#             cls.instance.__exists = True
            result = ''.join([cls.instance.__dict__[key], "(args: ", str(args), ", kwargs: ", str(kwargs), "). "]) 
            
            return result
        
if __name__ == '__main__':
    print MESSAGE('XLSXHandlerValueError', 'arg1', kwargs1 = '1')
            

