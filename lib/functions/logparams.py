#!/usr/bin/python

##############################################################################
# Removal of the "__license__" or "Freelancer_Perpetual_License.py" from 
# "__license__", or removal of "__author__" in this or any constituent 
# component or file constitutes a violation of the licensing and copyright 
# agreement.
__author__      = "Mike Rightmire"
__copyright__   = ""
__license__     = "Perpetual_License"
__version__     = "0.9.0.0"
__maintainer__  = ""
__email__       = ""
__status__      = "Beta"
##############################################################################

def logparams(self, _dict):
    for p in _dict:
        if ((p is not "self") and (not p.startswith('pas'))):
            self.log.debug("Parameter passed '" + p + "'=" + str(_dict[p]))