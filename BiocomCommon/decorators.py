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
