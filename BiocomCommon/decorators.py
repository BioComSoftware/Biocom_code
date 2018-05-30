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
__version__     = "0.9.0.0"
__maintainer__  = "Mike Rightmire"
__email__       = "Mike.Rightmire@BiocomSoftware.com"
__status__      = "Development"

##############################################################################

def decorate_all_class_methods(decorator):
    """
    :NAME:
        decorate_all_class_methods(decorator)
        
    :DESCRIPTION:
        decorate_all_class_methods is a class decorator intended to decorate
        *ALL* of a class's methods with said decorator, regardless of whether 
        it is already decorated (including with @classmethod or @staticmethod).
        
        While it will function with method objects that are not already
        decorated (untested), this would not be the approproate class decorator
        unless your class has already decorated methods. 
           
    :ARGUMENTS:
        None
        
    :VARIABLES:
        None 
        
    :RETURNS:
        The result of the finally called method.                  

    :USAGE:
        from common.decorators import decorate_all_class_methods
        import functools
        import unittest
        
        def add_arguments(func):
            @functools.wraps(func)
            def wrapped(self, *args, **kwargs):
                *do extra stuff*
                 return func(self, *args, **kwargs)
            return wrapped

        @decorate_all_class_methods(add_arguments)    
        class MESSAGE(object):
            @classmethod
            def TEMPLATE(self, *args, **kwargs):
                return "This is a template of a pre-digested message."

    """

    def decorate(cls):

        for attr in cls.__dict__:
            possible_method = getattr(cls, attr)
            if not callable(possible_method):
                continue
 
            # staticmethod
            if not hasattr(possible_method, "__self__"):
                raw_function = cls.__dict__[attr].__func__
                decorated_method = decorator(raw_function)
                decorated_method = staticmethod(decorated_method)
 
            # classmethod
            if type(possible_method.__self__) == type:
                raw_function = cls.__dict__[attr].__func__
                decorated_method = decorator(raw_function)
                decorated_method = classmethod(decorated_method)


            # instance method
            elif possible_method.__self__ is None:
                decorated_method = decorator(possible_method)

            setattr(cls, attr, decorated_method)

        return cls

    return decorate
