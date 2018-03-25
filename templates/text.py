print "_description = ''.join([\"BibliospecBridge(Class) is a Python bridge for \", \"sending and receiving results from the various 'BiblioSpec' binaries. \"]) \n"
print "    # Argument parser \n" 
print " \n"
print "    #=== REMEMBER !! =========================================================== \n"
print "    # If you change the defaults here, be sure to change the defaults in the  \n"
print "    # __init__ and in the set() method...since these are only called at the  \n"
print "    # command line \n"
print "    #=========================================================================== \n"
print "    parser = argparse.ArgumentParser(description=_description) \n"
print " \n"
print "    # GENERAL BibliospecBridge Argparse params \n"
print "    parser.add_argument(\"--tool\", action=\"store\", dest=\"tool\", \n"
print "                        required=True, \n"
print "                        help=''.join([\"The name of the BiblioSpec tool to be run. \"]) ) \n"
print " \n"