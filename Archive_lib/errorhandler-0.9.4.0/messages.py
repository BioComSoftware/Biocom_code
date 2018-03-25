##############################################################################
# Removal of the "__license__" line or content from  "__license__", or removal
# of "__author__" in this or any constituent # component or file constitutes a
# violation of the licensing and copyright agreement.
__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = "Telemend"
__license_file__= "Clause1.PERPETUAL_AND_UNLIMITED_LICENSING_TO_THE_CLIENT.py"
__version__     = "0.9.4.0"
__maintainer__  = "Mike Rightmire"
__email__       = "Mike.Rightmire@BiocomSoftware.com"
__status__      = "Development"
##############################################################################

from distutils.cmd import Command
import unittest


class MESSAGE(object):
    """
            log.error(MSG.triggerPhrase(args, kwargs))

    """    
    @classmethod
    def TEMPLATE(self, *args, **kwargs):
        message = "This is a template of a pre-digested message."
        message = ''.join([message, "args:'", str(args), "', ", "kwargs:'", str(kwargs), "', " ])
        return message
    
    @classmethod
    def NoConfDirCantCreate(self, *args, **kwargs):
        message = "'./conf/' directory does not exist  and cannot be created. A configuration file is mandatory. Please contact your administrator. Aborting run."
        message = ''.join([message, "args:'", str(args), "', ", "kwargs:'", str(kwargs), "', " ])
        return message
    
    @classmethod
    def CantOpenOrCreateFile(self, *args, **kwargs):
        message = "Unable to open or create the file for writing. Please contact your administrator. Aborting run."
        message = ''.join([message, "args:'", str(args), "', ", "kwargs:'", str(kwargs), "', " ])
        return message

    @classmethod
    def CannotFindConfigFile(self, *args, **kwargs):
        message = "DentrixReporting(main): 'config_file' is not a proper file, does not exist, or is in an improper location. Configuration files always reside in './conf'."
        message = ''.join([message, "args:'", str(args), "', ", "kwargs:'", str(kwargs), "', " ])
        return message

    @classmethod
    def DEFAULT_CONFIG_FILE(self, *args, **kwargs):
        message = ''.join([
            "# ---------------------------------------------------------------------\n", 
            "# Class configuration file ", 
            "# ---------------------------------------------------------------------\n", 
            "#######################################################################\n", 
            "# THIS FILE SHOULD ONLY BE USED TO SET SIMPLE CONFIGURATION VALUES.\n", 
            "# NOT AS A REPLACEMENT FOR SETTING VARIABLES PROPERLY WITHIN A CLASS!!\n", 
            "#\n", 
            "# THE PARAMETERS SET BY CONFIGHANDLER USING THIS FILE ARE SET DIRECTLY\n",  
            "# IN THE CALLING CLASS'S 'self'. PLEASE BE AWARE WHEN CREATING THIS\n",
            "# CONFIG FILE\n",
            "#######################################################################\n", 
            "#\n",
            "#  I.e. The line 'option = 1' in this file creates\n", 
            "#       'callingobject.self.option = 1' \n",
            "#       AND \n",
            "#       'callingobject.self._config.option = 1'.\n", 
            "#\n",
            "#  class some_python_class(object):\n",
            "#    def __init__(self):\n",
            "#      ConfigHandler(self, config_file = '/dir/dir/file.conf')\n",
            "# \n",
            "#  print self.option\n",
            "#  1\n",
            "#   \n",
            "#  print self._config.option\n",
            "#  1\n",
            "#\n",
            "# SECTIONS:\n",
            "#  Each [SECTION] defines a specific set of option-value pairs. The\n", 
            "# SECTION name is userspace and arbitrary. \n",
            "#\n",
            "# OPTIONS:\n",
            "#  option=value\n",
            "#   Each option within a section will create a variable BY THE SAME\n", 
            "#   NAME AS THE 'OPTION' in the instantiated ConfigHandler OBJECT with \n",
            "# its value set to 'value'. \n",
            "# I.e.\n",
            "#  'name=Hydrogen' creates a variable called 'self.name' in the\n", 
            "#  ConfigHandler object with the value of 'Hydrogen'. \n",
            "#  This is the same as if the line of code 'self.name = str('Hydrogen')'\n", 
            "#  had been written directly into the calling objects code.  \n",
            "#\n",
            "#   Caveats:\n",
            "#     - Spaces after the '=' are ignored.\n",
            "#\n",
            "#     - ALL VALUES ARE A STRING...so they MAY have to be converted for\n", 
            "#       use. At instantiation, ConfigHandler attempts to convert floats, \n",
            "#       integers and boolean - but be prepared to check for this. \n",
            "#\n",
            "#     - Numbers will be returned as floats or int...never bools.\n", 
            "#\n",
            "#     - Quotes around values will be returned as part of the string.\n", 
            "#\n",
            "# \n", 
            "# FORMAT:\n",
            "#  [section_name]\n",
            "#    option=value\n",
            "#\n",
            "#  - Lines starting with '#' are ignored.\n", 
            "#\n",
            "#  - Lines with '#' AFTER DATA ARE *NOT* IGNORED.\n", 
            "#    I.e. name=Hydrogen # This comment will be included in name's value\n",
            "#\n",
            "#  - Do NOT use quotes for text values.\n", 
            "# ---------------------------------------------------------------------\n",
            "[DEFAULTS]\n",
            "testvar = from auto configuration\n",
            ])
        return message


if __name__ == '__main__':
    import inspect
    print 
    members = inspect.getmembers(MESSAGE, predicate=inspect.ismethod)
    for i in members: 
        print i[0] + ':',
        command = 'MESSAGE.' + str(i[0])
        print eval(command)()
    print 'OK'
