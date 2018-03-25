##############################################################################
# Removal of the "__license__" line or content from  "__license__", or removal 
# of "__author__" in this or any constituent # component or file constitutes a 
# violation of the licensing and copyright agreement. 
__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = "Tesera"
__license_file__= "Clause1.PERPETUAL_AND_UNLIMITED_LICENSING_TO_THE_CLIENT.py"
__version__     = "0.9.3.0"
__maintainer__  = "Mike Rightmire"
__email__       = "Mike.Rightmire@BiocomSoftware.com"
__status__      = "Development"
##############################################################################

from checks         import checkObject
from checks         import fileExists
from checks         import checklist
from ConfigParser   import SafeConfigParser
from errorhandler   import handlertry
from errorhandler   import raisetry
from loghandler     import SetLogger

import ConfigParser 
import re
import types
import sys
from types import ModuleType

# class module(ModuleType):
#     """Automatically import objects from the modules."""
#     def __getattr__(self, name):
#         if name in object_origins:
#             module = __import__(object_origins[name], None, None, [name])
#             for extra_name in all_by_module[module.__name__]:
#                 setattr(self, extra_name, getattr(module, extra_name))
#             return getattr(module, name)
# #         elif name in attribute_modules:
# #             __import__('werkzeug.' + name)
#         return ModuleType.__getattribute__(self, name)

class GettattrWrapper(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped
        
    def __getattr__(selfself, name):
        print "GettattrWrapper...searching ", name #333
        try:
            return self._config.__dict__[name]
        except (AttributeError, NameError), e:
            raise AttributeError        
    
class ConfigHandler(object):
    """
    :NAME:
        ConfigHandler(callobj, *args, **kwargs)
        
    :DESCRIPTION:
        ConfigHandler() is a 'suite' configuration handler. It is intended to be 
        called by a class's "__init__" and set the configuration parameters 
        throughout an entire software package (I.e. the same configuration 
        information for every class object that is instantiated in association 
        with a complete piece of functional software).
        
        The primary goal with ConfigHandler is to load a single, consistent
        configuration environment to be passed amongst ALL objects within a 
        package.
        
        ConfigHandler is a SINGLETON, meaning once instantiated, THE SAME OBJECT
        will be returned to every class object calling it. 
        
        ConfigHandler initiates the "loghandler.SetLogger" method (a logging 
        handler which is ALSO  a singleton and ALSO intended to be a consistent 
        single logging object passed amongst all instantiated objects of a 
        package. If you are calling ConfigHandler, you do not need to separately
        call loghandler.SetLgger in any classes that use the ConfigHandler
        object.     
        
    :ARGUMENTS:
        callobj:    The "self" of the __init__ that is calling ConfigHandler 
                    (NOT ConfigHandler's 'self'.) ConfigHandler MODIFIES THE 
                    CALLER'S SELF by adding the "self.log" variable, a 
                    "self._config" variable, and setting a 
                    "self.config_file_variable" into the calling objects self
                    for every variable found in the config file. 
                    
                    For this reason IT'S VERY IMPORTANT that parameters set by 
                    the <project>.conf FILE DO NOT CONFLICT WITH any variables 
                    manually coded into the calling object.
                    
                    The fact that the config file variables will SUPERCEDE any
                    self.variables set in the calling object is very 
                    intentional and should not be workaround-ed.      
                    
        *args, **kwargs: 
            Numerous parameters can be passed into the ConfigHandler object.
            
            Using args/kwargs for even the one mandatory parameter was chosen 
            to allow for future flexibility.  
            
            MANDATORY: The only mandatory argument to ConfigHandler is 
                       'config_file' which is the full path to the 
                       configuration.conf file.  
    
    :VARIABLES:
        No userspace mutable variables. 
        
    :METHODS:
        No userspace mutable methods...although future version of this will 
        have methods for setting and getting variables as well as manipulating 
        the overall config environment including making changes to the config 
        file and reloading config parameters. 

    :RETURNS:
        self as callingobject._config
        
    :USAGE:
        <myClass>
            def __init__(self):
                self.optional_var = ConfigHandler(config_file = "./my.conf)
                
    :EXAMPLE:
        <configuration.conf>
        # ---------------------------------------------------------------------
        # Class configuration file 
        # ---------------------------------------------------------------------
        #######################################################################
        #  THIS FILE SHOULD ONLY BE USED TO SET SIMPLE CONFIGURATION VALUES. 
        # NOT AS A REPLACEMENT FOR SETTING VARIABLES PROPERLY WITHIN A CLASS!! 
        #
        # THE PARAMETERS SET BY CONFIGHANDLER USING THIS FILE ARE SET DIRECTLY 
        # IN THE CALLING CLASS'S "self". PLEASE BE AWARE WHEN CREATING THIS 
        # CONFIG FILE 
        #######################################################################
        #
        #  I.e. The line "option = 1" in this file creates 
        #       "callingobject.self.option = 1" 
        #       AND 
        #       "callingobject.self._config.option = 1". 
        #
        #  class some_python_class(object):
        #    def __init__(self):
        #      ConfigHandler(self, config_file = "/dir/dir/file.conf")
        # 
        #  print self.option
        #  1
        #   
        #  print self._config.option
        #  1
        #
        # SECTIONS:
        #  Each [SECTION] defines a specific set of option-value pairs. The 
        # SECTION name is userspace and arbitrary. 
        #
        # OPTIONS:
        #  option=value
        #   Each option within a section will create a variable BY THE SAME 
        #   NAME AS THE 'OPTION' in the instantiated ConfigHandler OBJECT with 
        # its value set to "value". 
        # I.e.
        #  "name=Hydrogen" creates a variable called "self.name" in the 
        #  ConfigHandler object with the value of "Hydrogen". 
        #  This is the same as if the line of code 'self.name = str("Hydrogen")' 
        #  had been written directly into the calling objects code.  
        #
        #   Caveats:
        #     - Spaces after the "=" are ignored.
        #
        #     - ALL VALUES ARE A STRING...so they MAY have to be converted for 
        #       use. At instantiation, ConfigHandler attempts to convert floats, 
        #       integers and boolean - but be prepared to check for this. 
        #
        #     - Numbers will be returned as floats or int...never bools. 
        #
        #     - Quotes around values will be returned as part of the string. 
        #
        #  
        # FORMAT:
        #  [section_name]
        #    option=value
        #
        #  - Lines starting with "#" are ignored. 
        #
        #  - Lines with "#" AFTER DATA ARE *NOT* IGNORED. 
        #    I.e. name=Hydrogen # This comment will be included in name's value
        #
        #  - Do NOT use quotes for text values. 
        # ---------------------------------------------------------------------
        [LOGGING]
        logfile             = MyPackage.log
        log_path            = /shared/MyPackage/var/log/
        app_name            = MyPackageName 
        log_level           = 10 
        screendump          = True
        create_paths        = False         
    """
    __exists = False
    
    def __new__(cls, callobj, *args, **kwargs): 
        """
        This is a singleton class. 
        
        The __new__ method is called prior to instantiation with __init__. 
        If there's already an instance of the class, the existing object is 
        returned. If it doesn't exist, a new object is instantiated with 
        the __init__.
        """
        # __init__ is called no matter what, so...
        # If there is NOT an instance, just create an instance 
        # This WILL run __init__
        if not hasattr(cls, 'instance'):
            cls.instance = super(ConfigHandler, cls).__new__(cls)
            callobj._config = cls.instance
            return cls.instance

        # Else if an instance does exist, set a flag since
        # __init__is called, but flag halts completion (just returns)
                   
        else:
            cls.instance.__exists = True
            callobj._config = cls.instance
            return cls.instance

    def __init__(self, callobj, *args, **kwargs):
        """"""

        sys.modules[callobj.__class__.__module__] = GettattrWrapper(sys.modules[callobj.__class__.__module__])
        
#         sys.modules[__name__] = ModuleWrapper(sys.modules[__name__])
        
        # Here, we do not give the option of changing the ConfigHandler 
        # parameters. One log file, determined by the main application
        # This can be changed to match SetLogger...but is not recommended.        
        if self.__exists:
            callobj.log = self.log            
            return
        
        try:
            self.log_level = kwargs["log_level"]
        except (KeyError, AttributeError), e:
            self.log_level = 40

        try:
            self.screendump = kwargs["screendump"]
        except (KeyError, AttributeError), e:
            self.screendump = False
        
        self.log = SetLogger(
                             app_name = "configparser", 
                             logfile = "configparser.log",
                             log_path = "./", 
                             log_level = self.log_level, 
                             screendump = self.screendump, 
                             create_paths = False 
                             )


        try:
            self.config_file    = kwargs["config_file"]
        except (KeyError, AttributeError), e:
            e = ''.join(["Parameter 'config_file' ", 
                         "MUST be passed at first object instantiation.", 
                         str(e)])
            raise ValueError(e)

        self.log.info("ConfigHandler called with " + str(self.config_file))

        self._load_all_vars()

#         # Override config file vars. This needs to come AFTER loding the config 
#         # file but BEFORE the final SetLogger to allow for config file vars 
#         # to be manually overidden  
#         if log_level    is not None: self.log_level = log_level
#         if screendump   is not None: self.screendump = screendump

        self._override_with_kw_vars(kwargs)

        self._set_mandatory_defaults({"app_name":"configparser", 
                                      "logfile":"configparser.log", 
                                      "log_path":"./", 
                                      "create_paths":False} 
                                     )

#         callobj.__dict__.update(self.__dict__) #333 reinstate me if nec

        self.log = SetLogger(
                             app_name = self.app_name, 
                             logfile = self.logfile,
                             log_path = self.log_path, 
                             log_level = self.log_level, 
                             screendump = self.screendump, 
                             create_paths = self.create_paths 
                             )
        
        callobj.log = self.log
        
        

    
    #__________________________________________________________________________
    # PRIVATE METHODS
        
    @handlertry("PassThroughException:")    
    def _convert_string_values(self, value):
        """"""
        @raisetry(''.join(["ConfigHandler._convert_values; checking value of '", 
                           str(value), "'."]))
        def _convertit(self, value):
            # Check for boolean text, return actual bool
            if (re.match("^true$", str(value).lower())) : return True
            if (re.match("^false$", str(value).lower())): return False

            # Check for INT and float 
            if (re.match("^[0-9]+\.[0-9]*$", value)):   return float(value)
            if (re.match("^[0-9]+$", value)):           return int(value)

            # Otherwise just return original string, no conversion            
            return value 
        
        result = _convertit(self, value)

        return result
            
    @handlertry("")    
    def _load_all_vars(self):
        """"""
        self.open_file()
        self.loadattr()

    @handlertry("FATAL:")
    def _override_with_kw_vars(self, kwargs):
        for key in kwargs.keys():
            self.__dict__[key] =  kwargs[key]
        return True
        
        
    #__________________________________________________________________________
    # PUBLIC METHODS

    @handlertry("PassThroughException: rhandler._set_mandatory_defaults")
    def _set_mandatory_defaults(self, _dict):
        """
        """
        for key in _dict.keys():
            if key not in self.__dict__.keys():
                self.__dict__[key] = _dict[key]
        return

    @handlertry("PassThroughException:")    
    def get(self, varname, default = None):
        """
        Retrieves the attribute from ConfigHandlers "self"
        """
        # If the first attempt to return a self var fails, control 
        # should pass to @handlertry where corrections can be set 
        # For now this is just a passthrough, which will drop control
        # to the second line, which returns the default
        return self.__dict__[varname]
        return default

    @handlertry("PassThroughException:")    
    def set(self, varname, value, default = None):
        """
        Sets an attribute from ConfigHandlers "self"
        """
        self.__dict__[str(varname)] = value
        return True

    @handlertry("PassThroughException:")    
    def getconfig(self, section = None, valuename = None, persist = False):
        """
        """
        raise NotImplementedError

    @handlertry("PassThroughException:")    
    def setconfig(self, section = None, valuename = None, persist = False):
        """
        """
        raise NotImplementedError
    
    @handlertry("ConfigFileParseError: ")
    def open_file(self):
        self.verify_file()
        self.log.debug(("Opening " + str(self.config_file)))
        self.config = SafeConfigParser()
        self.config.optionxform = str
        self.config.read(self.config_file)
        return True
    
    @handlertry(''.join(["ConfigFileNoOption:"]))        
    def loadattr(self, varname = None, section = None):
        """
        Retrieves a variable from the CONFIG FILE (not self)
        """
        _found = False
        for section_name in self.config.sections():

            if ((section_name.lower() == str(section).lower()) or 
                (section is None)):
                
                for name, value in self.config.items(section_name):
                    if ({"LOADALL":True, None:True, name:True}.get(varname)):
                        value = self._convert_string_values(value)
                        self.__dict__[name] = value
#                         self.log.debug(''.join(["set '", str(name), 
#                                                 "' to '", str(value),
#                                                 "'."]))
                        _found = True

                        if varname is not None: return value

        if not _found: raise AttributeError(''.join(["Unable to find variable '",
                                                    str(varname), 
                                                    "' in section '", 
                                                    str(section), 
                                                    "' of config_file '", 
                                                    str(self.config_file), 
                                                    "'. "
                                                    ]))
            
    @handlertry("PassThroughException:")    
    def verify_file(self):
        """"""
        self.log.debug(("Verfiying " + str(self.config_file)))
        # Check config file exists since parser will not error if you 
        # attempt to open a non-existent file
        if not fileExists(self.config_file):
            e = ''.join(["ConfigFileNotFound(", 
                         str(self.config_file),"):"])
            raise IOError(e) # Remove me and active self.err line

        
if __name__ == "__main__":
    from loghandler import SetLogger
     
    class forttest(object):
        def __init__(self):

            self.config = ConfigHandler(
                                        self, 
                                        log_level = 10,
                                        screendump = True,
                                        config_file = "../etc/MRAT.conf"
                                        )

    obj = forttest()
    
