#!/usr/bin/python

__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = "BioCom_Commercial_Copyright.py"
__version__     = "0.9.0.0"
__maintainer__  = "Mike Rightmire"
__email__       = "rightmirem@utr.net"
__status__      = "Test"


import mechanize
from lib import check_verbose_object
from lib import checkurl as _checkurl
from errors import *

#### FOR TEST AND DEBUG ONLY ####
import sys, logging
logger = logging.getLogger("mechanize")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)
####

class Scraper(object):
    """
    Scraper()
    Super CLASS
    The "Scraper" object is a base class to handle the basic browser tasks 
    of manipulating web pages. It contains the cookes and the HTML response, 
    lending it to further manipulation.
    
    Methods:
    
    Variables:
    """
    def __init__(self, verbose = None):
        self.verbose    = check_verbose_object(verbose) # Logging object
        self.vlog       = self.verbose.vlog()       # Set logfile shortcut
        self.vscreen    = self.verbose.vscreen()    # Set screen print shortcut
        self.browser = mechanize.Browser()      #Set the browser
        self.browser.set_handle_robots(False)   # Don't ident as a robot
        self.browser.set_handle_refresh(False)  # sometimes hangs without this
        self.browser.set_handle_referer(True)
        self.browser.follow_meta_refresh = True
        headerstring = ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1)' + 
                        ' Gecko/2008071615' + 
                        ' Fedora/3.0.1-1.fc9' + 
                        ' Firefox/3.0.1')
        self.browser.addheaders = [('User-agent', 
                                    headerstring)]
        self.cookiejar = mechanize.CookieJar()
        self.the_page = None

    
    def checkurl(self, URL):
        """"""
        if _checkurl(URL): return URL
        if "http" not in str(URL).lower(): URL = "http://" + str(URL)
        if _checkurl(URL): return URL
        else: raise URLNotFormatted(str(URL))

    def getcontrols(self):
        """"""
        _list = []
        try:
            for c in self.browser.form.controls:
                _list.append(str(c))
            return _list
        except AttributeError, e:
            if 'NoneType' in str(e):raise FormNotSelected(e)
                
    def getforms(self):
        """"""
        forms = []
        try:
            for form in self.browser.forms():
                forms.append(form.name)
            return forms
        except AttributeError, e:
            if 'NoneType' in str(e):raise URLNotSelected(e)    

    def getformfields(self):
        """"""
        _list = []
        try:
            for c in self.browser.form.controls:
                try: # Catches final item which is 'None'
                    _list.append(c.__dict__['attrs'])
                except KeyError, e:
                    return _list
        except AttributeError, e:
            if 'NoneType' in str(e):raise FormNotSelected(e)
                     
    def getpage(self):
        """"""
        response = self.browser.response()
        the_page = response.read()
        return the_page

    def geturl(self):
        """"""
        response = self.browser.geturl()
        return response

    def login(self, form_name, user_field, user, pwd_field, pwd): 
        response = self.submitform(form_name, 
                                   {user_field:user, pwd_field:pwd})
        return response 
    
    def searchforms(self, URL, form_name):
        """"""
        if form_name is not None:
            self.browser.select_form(form_name)
            self.browser.set_all_readonly(False) 
        self.browser.select_form(nr=0)
        self.browser[form_input_name] = form_search_term
        results = self.browser.submit()
        return results.read()

    def setpage(self, URL):
        URL = str(URL)
        URL = self.checkurl(URL) 
        request = mechanize.Request(URL)
        self.cookiejar.add_cookie_header(request)
        self.the_page = self.browser.open(request)
        return self.the_page

    def setform(self, form_name):
        response = self.browser.select_form(form_name)
        return response
    
    def submitform(self, form_name, _dict):
        """
        """
        self.browser.select_form(str(form_name))
        loop = True
        try:
            while loop:
                field_name, field_data = _dict.popitem()
                self.browser[str(field_name)] = str(field_data)
        except KeyError: # Empty dictionary
            loop = False
        except Exception, e:
            error = str(e) + "\nField name and value must be passed as dictionary key:value pairs"
            raise TypeError(error)
        self.browser.method = "POST"
        response = self.browser.submit().read()
        return response

# Main for testing
if __name__ == "__main__":
    s = Scraper()
    s.setpage("http://www.elance.com/myelance")
    l = s.getforms()
    print l
    r = s.setform('loginForm')
    l = s.getformfields()
    for i in l:
        print i
    
    pass # Always leave this pass
