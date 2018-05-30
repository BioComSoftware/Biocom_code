##############################################################################
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU LGPL License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# See the files gpl.txt and lgpl.txt packaged with this file.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = "LGPLv3"
__license_file__= "lgpl.txt"
__version__     = "0.9.7.2"
__maintainer__  = "Mike Rightmire"
__email__       = "Mike.Rightmire@BiocomSoftware.com"
__status__      = "Development"

##############################################################################

from BiocomCommon.confighandler import ConfigHandler

import inspect

# THESE MUST ALL BE LISTS OF STRINGS!!!!
whitelist_chars_default = []
whitelist_words_default = [] 
blacklist_chars_default = ["<",">", ";"] 
blacklist_words_default = [ 
                            'su', 
                            'sudo', 
                            'rm', 
                            'mkfs', 
                            'dd', 
                            'fork', 
                            'while', 
                            'tar', 
                            'wget', 
                            'sh', 
                            'csh', 
                            'tsh', 
                            'bash', 
                            'python',
                            'perl',
                            'chmod', 
                            'chown', 
                            '__attribute__', 
                            ]

def _split_to_char_and_word(L):
    L = _stringlist(L)
    #===========================================================================
    # if not isinstance(L, list):
    #     err = ''.join(["Parameter must be a list of strings. (L='", str(L), "')."])
    #     raise ValueError(err)
    #===========================================================================
    # Parse for characters and strings
    L_chars = [] 
    L_words = []             
    for item in L:
        if    len(item) < 1: continue
        elif  len(item) < 2: L_chars.append(item)
        L_words.append(item) # always add 
    
    #===========================================================================
    # L_chars = _stringlist(L_chars)
    # L_words = _stringlist(L_words)
    #===========================================================================
    
    return L_chars, L_words

def _stringlist(data):
    """"""
    if isinstance(data, list): 
        _list = data
    # If dict, values only are checked
    elif isinstance(data, dict): 
        for value in data.values(): 
            _list.append(value)
    # If anything else, list of strings
    else:  _list = str(data).split() 

    _return_list = []
    for item in _list:
        _return_list.append(str(item).lower())
    
    return _return_list
        
def sanitize(data, blacklist = False, whitelist = False, error = True):
        """
        Set defaults
        """
        config = ConfigHandler()
        
        # First check for configfile of just blacklist (not word or char)
        if config.blacklist: 
            blacklist_chars, blacklist_words =  _split_to_char_and_word(config.blacklist)
        # check for config file blacklist_chars. This will override config file blacklist alone. 
        # if NOT elif
        if config.blacklist_chars: 
            blacklist_chars = _stringlist(config.blacklist_chars)
        else:     
            blacklist_chars = _stringlist(blacklist_chars_default)
        # Blacklist_chars is now set by default. 
        # Now blacklist words
        # if NOT elif
        if config.blacklist_words: 
            blacklist_words = _stringlist(config.blacklist_words) 
        else:                           
            blacklist_words = _stringlist(blacklist_words_default)
        # Blacklist_words is now set by default.
        # FINALLY, if overrides were passed in, use them instead 
        if   blacklist: 
            blacklist_chars, blacklist_words =  _split_to_char_and_word(blacklist)
        
        # Next whitelist
        # First check for configfile of just whitelist (not word or char)
        if config.whitelist: 
            whitelist_chars, whitelist_words =  _split_to_char_and_word(config.whitelist)
        # check for config file whitelist. This will override config file whitelist alone. 
        # if NOT elif
        if config.whitelist_chars: 
            whitelist_chars = _stringlist(config.whitelist_chars)
        else:                           
            whitelist_chars = _stringlist(whitelist_chars_default)
        # whitelist_chars is now set by default. 
        # Now whitelist words
        # if NOT elif
        if config.whitelist_words: 
            whitelist_words = _stringlist(config.whitelist_words) 
        else:                           
            whitelist_words = _stringlist(whitelist_words_default)
        # Blacklist_words is now set by default.
        # FINALLY, if overrides were passed in, use them instead 
        if   whitelist: 
            whitelist_chars, whitelist_words =  _split_to_char_and_word(whitelist)
        
        # whitelist_words are parsed as words, however whitelist_chars are 
        # simple subtracted from the blacklist_chars
        _tmp_list = []
        for c in blacklist_chars: 
            if c not in whitelist_chars: _tmp_list.append(c)
        blacklist_chars = _tmp_list
        
        # Make stringlists
        
        print '__new__.blacklist_chars = ', blacklist_chars #333
        print '__new__.blacklist_words = ', blacklist_words #333
        print '__new__.whitelist_chars = ', whitelist_chars #333
        print '__new__.whitelist_words = ', whitelist_words #333

        _datalist = _stringlist(data) 
        print '_datalist = ', _datalist #3333
        # Start with whitelist words. If a white list is included, then each 
        # item in the data must be in the whitelist
        if whitelist_words:
            for word in _datalist:
                # All the words in the _datalist must be in the whitelist if it is passed 
                if word.lower() not in whitelist_words:
                    print 'bad word not in whitelist:', word #3333 
                    return False
        # Whitelist CHARACTERS, on the other hand, are just subtracted from 
        # the blacklist characters
        
        # Parse each word in passed in data
        for word in _datalist:
            # Check each word again word blacklist
            if word.lower() in blacklist_words: return False
            # and check each word for illegal characters
            for c in word.lower():
                if c in blacklist_chars: return False
                
        # If here, alles ist gut!
        return True
    
if __name__ == '__main__':
    print sanitize('This is OK  ', whitelist = ['this', 'is', 'ok',])