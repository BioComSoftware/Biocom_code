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
__status__      = "Development"
##############################################################################

import json
import requests
import sys

from checkurl   import checkurl as _checkurl
from errors     import *
from verbose    import verbose
from verbose    import checkverbose

#### FOR TEST AND DEBUG ONLY ####
# import sys, logging
# logger = logging.getLogger("requests")
# logger.addHandler(logging.StreamHandler(sys.stdout))
# logger.setLevel(logging.DEBUG)
####

class APIengine(object):
    """
    Scraper()
    Super CLASS
    The "Scraper" object is a base class to handle the basic browser tasks 
    of manipulating web pages. It contains the cookes and the HTML response, 
    lending it to further manipulation.
    
    Methods:
    
    Variables:
    """
    def __init__(self):
        
        # Set logging
        verbose(self, self.__class__.__name__, loglevel = 10, screen = True)
        self.vout.debug("Logging enabled.")

        self.pagedata = None
        self.err = errors(self)

        # Set browser session
        self.br = requests.Session()
        
        #Set session headers
        headers = {}
        headers['content-type'] = "application/json"
        headers['User-agent']   = ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1)' + 
                ' Gecko/2008071615' + 
                ' Fedora/3.0.1-1.fc9' + 
                ' Firefox/3.0.1')
        self.br.headers.update(headers)

    def checkurl(self, URL):
        """"""
        if "http" not in URL: 
            msg = ("'http://' does not appear to be a part of the passed " + 
                   "URL (" + str(URL) + "). Adding 'http://' by default.")
            self.vout.info(msg)
            URL = "http://" + str(URL)
            
        if _checkurl(self, URL): 
            return URL
        else: 
            e = "URLNotFormatted: (" + (str(URL)) + ")"
            self.err.handle(e)

    def getforms(self):
        """"""
        raise NotImplementedError    

    def getformfields(self):
        """"""
        raise NotImplementedError    
                     
    def getpage(self):
        """"""
        try:
            return self.pagedata.content
        except AttributeError, e:
            e = "URLNotSelected: " + str(e)
            self.err.handle(e)

    def geturl(self):
        """"""
        try:
            return self.pagedata.url
        except AttributeError, e:
            e = "URLNotSelected: " + str(e)
            self.err.handle(e)

    def login(self, form_name, user_field, user, pwd_field, pwd): 
        raise NotImplementedError    

#         response = self.submitform(form_name, 
#                                    {user_field:user, pwd_field:pwd})
#         return response 
    
    def searchforms(self, URL, form_name):
        """"""
        raise NotImplementedError    

    def setpage(self, URL):
        URL = str(URL)
        URL = self.checkurl(URL) 
        self.pagedata = self.br.get(URL)
        return self.pagedata

    def setform(self, form_name):
        raise NotImplementedError    
    
    def submitform(self, form_name, _dict):
        """
        """
        raise NotImplementedError    

#         self.browser.select_form(str(form_name))
#         loop = True
#         try:
#             while loop:
#                 field_name, field_data = _dict.popitem()
#                 self.browser[str(field_name)] = str(field_data)
#         except KeyError: # Empty dictionary
#             loop = False
#         except Exception, e:
#             error = str(e) + "\nField name and value must be passed as dictionary key:value pairs"
#             raise TypeError(error)
#         self.browser.method = "POST"
#         response = self.browser.submit().read()
#         return response

# Main for testing

if __name__ == "__main__":
    s = APIengine()
    URL = 'www.google.com'
    r = s.setpage(URL)
    r = s.geturl()
    print r
#     s.setpage("http://www.elance.com/myelance")
#     l = s.getforms()
#     print l
#     r = s.setform('loginForm')
#     l = s.getformfields()
#     for i in l:
#         print i
    
    pass # Always leave this pass
