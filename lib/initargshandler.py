import inspect
import functools

def store_args(method):
    """
    Stores provided method args as instance attributes.
    EXAMPLE:
        class A:
            @store_args
            def __init__(self, a, b, c=3, d=4, e=5):
                pass
    
        a = A(1,2)
        print(a.a, a.b, a.c, a.d, a.e)
        
        Result will be 1 2 3 4 5 on Python3.x 
        or (1, 2, 3, 4, 5) on Python2.x
        
    Thanks to davidbonnet at http://stackoverflow.com/questions/6760536/python-iterating-through-constructors-arguments    
    """
    argspec = inspect.getargspec(method)
    defaults = dict(zip( argspec.args[-len(argspec.defaults):], argspec.defaults ))
    arg_names = argspec.args[1:]
    @functools.wraps(method)
    def wrapper(*positional_args, **keyword_args):
        self = positional_args[0]
        # Get default arg values
        args = defaults.copy()
        # Add provided arg values
        list(map( args.update, ( zip(arg_names, positional_args[1:]), keyword_args.items() ) ))
        # Store values in instance as attributes
        self.__dict__.update(args)
        return method(*positional_args, **keyword_args)

    return wrapper