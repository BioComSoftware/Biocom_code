__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = "BioCom_GPL_Copyright.py"
__version__     = "0.9.0.0"
__maintainer__  = "Mike Rightmire"
__email__       = "rightmirem@utr.net"
__status__      = "Test"

import ast

# Type checks that use functional checks instead of isinstance or type
def _isdict(data):
    try: 
        data.keys()
        return True
    except AttributeError:
        return False

def _isstr(data):
    try: 
        data + "string test"
        return True
    except TypeError:
        return False
        
def _islist(data):
    try: 
        data.insert(0,"THIS_IS_FALSE_DATA_ADDED_AS_A_TEST")
        data.pop(0)
        return True
    except AttributeError or TypeError:
        return False
    
#To lists
def strToList(data, delim = " "):
    if _islist(data): return data
    if not _isstr(data): raise TypeError("str_to_list requires string input")
    else: data = data.split(delim);
    return data
    
# To Dictionaries 
def _literal_str_to_dict(data):
    if _isdict(data): return data
    data = ast.literal_eval(data)
    return data

def _assumptive_str_to_dict(data):
    if _isdict(data): return data
    data = str_to_list(data, ",")
    data = list_to_dict(data)
    return data

def listToDict(data):
    _dict = {}
    if _isdict(data): return data
    if _islist(data) is False: raise TypeError("str_to_list requires list input")
    loop = True
    while loop:
        try:
            key = data.pop(0)
            try:
                value = data.pop(0)
            except IndexError:
                value = None
            _dict[key] = value
        except IndexError:
            loop = False
    return _dict

def strToDict(data):
    if _isdict(data): return data
    data = "".join(c for c in data if c not in "\"\'\]\[")
    if ":" in data: return _literal_str_to_dict(data)
    else: return _assumptive_str_to_dict(data)
            
if __name__ == "__main__":
    d = str_to_dict("['a','b','c']")
    print "d = ", d