"""
unpassable toy implementation
"""
__version__ = '0.0.1'


class UP:

    def __repr__(self):
        return "<Unpassable>"

Unpassable =  UP()


from functools import wraps
from inspect import signature



def ignore_unpassable(fun):
    """
    decorate function `fun` to ignore any kwargs that is set to unpassable.
    """

    sig = signature(fun)
    accept_kw = len([p.kind is p.VAR_KEYWORD for p in sig.parameters.values()]) != 0

    @wraps(fun)
    def wrapper(*args, **kwargs):
        nargs = []
        for arg,(name, p )in zip(args, sig.parameters.items()):
            if (p.kind in (p.POSITIONAL_ONLY, p.VAR_POSITIONAL)) and (arg is Unpassable):
                raise TypeError('Unpassable cannot be passed as positional arg')
                nargs.append(arg)
            else:
              if p is not Unpassable:
                  kwargs[name] = arg
                  


        kw_copy = {k:v for k,v in kwargs.items() if v is not Unpassable }
        #print(nargs, kw_copy)
        return fun(*nargs, **kw_copy)

    return wrapper

