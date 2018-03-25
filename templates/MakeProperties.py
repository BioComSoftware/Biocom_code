
from BiocomCommon.checks import Checks
from BiocomCommon.loghandler import log

import re
import os
import inspect 
import ntpath

class test:
    def __init__(self, *Args, **kwargs):
        self.checks = Checks()
        self._slash      = self.checks.directory_deliminator()
        self.script      = inspect.getfile(inspect.currentframe())
        self.scriptname  = ntpath.basename(self.script).split('.')[0]
        self.script_path = os.getcwd()

        # Set logging defaults
        app_name     = kwargs.pop("app_name", self.scriptname) 
        logfile      = kwargs.pop("logfile", 'syslog')
        log_level    = kwargs.pop("log_level", 10)
        screendump   = kwargs.pop("screendump", True)
        create_paths = kwargs.pop("create_paths", False)
        
        log.info(
                  "Beginning execution: '" + str(self.scriptname) + "'. ",
                  app_name      = app_name,
                  logfile       = logfile, 
                  log_level     = log_level, 
                  screendump    = screendump,
                  )
        
    
if __name__ == '__main__':
    print 'Starting...'
    # Star new file
    outFH = open('MakeProperties-out.py', 'w+', 0)
    # Headers and imports
    outFH.write("import argparse"                   + "\n")
    outFH.write("import inspect"                    + "\n")
    outFH.write("import re"                         + "\n")
    outFH.write(                                      "\n")
    outFH.write("class testproperties(object):"     + "\n")
    outFH.write(                                      "\n")

    # Load variable names
    var_list = []
    with open('MakeProperties.txt', 'r', 0) as inFH:
        for line in inFH:
            # Line must be just variable names
            if len(line) > 1:
                # Truncate all spaces.
                sm_var = ''.join(c for c in line if c not in "     \n\r")
                var_list.append(sm_var)

        
    # Write properties
    for sm_var in var_list: 
        print "Writing @property lines for:", sm_var 
        bg_var = sm_var.upper()
        outFH.write("    @property\n")
        outFH.write("    def " + sm_var + "(self):\n")
        outFH.write("        try:\n")
        outFH.write("            return self." + bg_var   + "\n")
        outFH.write("        except (NameError, AttributeError) as e:" + "\n")
        outFH.write("            err = ''.join([self.__class__.__name__, \".\", inspect.stack()[0][3], \": '" + sm_var + "' is not yet set.\" ])\n") 
        outFH.write("            raise ValueError(err)\n")
        outFH.write("\n")
        outFH.write("    @" + sm_var + ".setter\n") 
        outFH.write("    def " + sm_var + "(self, value):\n")
        outFH.write("        self."+ bg_var + " = value\n")
                    # Additional specific stuff here
        outFH.write("        if re.match('^\s*OPTIONAL\s*$', value):\n")
        outFH.write("            self."+ bg_var + " = False\n")
        outFH.write("\n")
        outFH.write("    @" + sm_var + ".deleter\n")
        outFH.write("    def " + sm_var + "(self):\n")
        outFH.write("        del self."+ bg_var + "\n")
        outFH.write("\n")

    
    # Write main for testing
    outFH.write("if __name__ == '__main__':\n")
    outFH.write("    o = testproperties()\n")
    outFH.write("    _description = ''.join([\"Put the description lines here. \"]) \n")
    outFH.write("    # Argument parser \n") 
    outFH.write(" \n")
    outFH.write("    #=== REMEMBER !! =========================================================== \n")
    outFH.write("    # If you change the defaults here, be sure to change the defaults in the  \n")
    outFH.write("    # __init__ and in the set() method...since these are only called at the  \n")
    outFH.write("    # command line \n")
    outFH.write("    #=========================================================================== \n")
    outFH.write("    parser = argparse.ArgumentParser(description=_description) \n")
    outFH.write(" \n")
    for sm_var in var_list:
        outFH.write("    parser.add_argument(\"--" + sm_var + "\", action=\"store\", dest=\"" + sm_var + "\", \n")
        outFH.write("                        required=True, \n")
        outFH.write("                        help=''.join([\"Put the variable help here. \"]) ) \n")
        outFH.write(" \n")    
        
        #=======================================================================
        # outFH.write("    print '------------'\n")
        # outFH.write("    print '" + sm_var + " = value test ...' \n")
        # outFH.write("    o." + sm_var + " = 'test' \n")
        # outFH.write("    print 'value: ', o." + sm_var + "\n") 
        # outFH.write("    print 'Var = NULL test ...' \n")
        # outFH.write("    o." + sm_var + " = 'OPTIONAL' \n")
        # outFH.write("    print 'value: ', o." + sm_var + "\n") 
        # outFH.write("\n")
        #=======================================================================

    print 'DONE.'
            

    
