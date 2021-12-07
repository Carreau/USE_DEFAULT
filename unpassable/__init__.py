"""
unpassable toy implementation
"""
__version__ = '0.0.1'


Unpassable = object()


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

        for arg, param in zip(args, sig.parameters.values()):
            if (p.kind in p.POSITIONAL_ONLY) and (arg is Unpassable):
                raise TypeError('Unpassable cannot be passed as positional arg')

        kw_copy = {k:v for k,v in kwargs.items() if v is not Unpassable }
        return fun(*args, **kwargs)

