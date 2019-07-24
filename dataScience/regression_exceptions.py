import inspect

class regression_exception(Exception):
    def __init__(self, message = "", *args):
        # Capture the calling error, if it is captured by "except Exception as e"
        # Otherwise generic
        try: e = inspect.stack()[2][0].f_locals["e"]
        except: e = Exception()
        # Update the message with the original error
        message = ''.join([ str(message), " (" + str(type(e)) + ") " + str(e) ])
        # raise
        Exception.__init__(self, message, *args) 

class DFPropetyNotSetException(regression_exception):
    def __init__(self, message = "", *args):
        # Update the message
        message = ''.join(["The class parameter 'df' (The working pandas DataFrame) does not yet appear to be set. ", 
                           str(message),
                           ])
        #print("Run any extra code here")
        regression_exception.__init__(self, message, *args) 
    
class FeaturesPropetyNotSetException(regression_exception):
    def __init__(self, message = "", *args):
        # Update the message
        message = ''.join(["The class parameter 'features' does not yet appear to be set. ", 
                           str(message),
                           ])
        #print("Run any extra code here")
        regression_exception.__init__(self, message, *args) 

class TargetPropetyNotSetException(Exception):
    def __init__(self, message = "", *args):
        # Update the message
        message = ''.join(["The class parameter 'target' does not yet appear to be set. ", 
                           str(message),
                           ])
        #print("Run any extra code here")
        regression_exception.__init__(self, message, *args) 

