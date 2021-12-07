# USE_DEFAULT


Sentinel value to represent empty parameters.

I am sometime in the need to call a function to which I conditionally need to pass parameters that must use the function default value.

This often leads to overly verbose or complex code either calling the function with unpacking *args , **kwargs, or have conditional path depending on weather I want to pass the parameter.

Code example

On the callee side, this can often be made by either using a sentinel value, or accepting **kwargs and looking for the (absence) of a key.

While obviously None, or Ellipsis,  can be used as a sentinel value, they are valid parameters that can be passed to function, and thus make it difficult to know whether the default value vas used or passed explicitlely. Plus this requires the caller to make sure the default value in the underlying library does not change, and the callee's default value to represent no-par meters becomes part of it's API. 

One example is the "timeout" parameter of several 

Outer type stability.


This would also be particularly useful in high level API wrapper where default values are defined in lower level components, 

Def plot(x,y, color=null):
    Core.draw(...)


Assignment different than deleting. Unnamed error.
Dict literal.

Check for identity, still useful default.
In indexing operation/slice ?



https://github.com/numpy/numpy/blob/0bd7f2df20154370544925aacf7b1439d121cc53/numpy/ma/core.py#L1809-L1814


(which fun story...I put that in a few more places a few years ago and broke pandas because they were on import reloading numpy because ... pandas so if you did keepdims=_NoValue it would break because the _NoValue singleton would be reloaded in import, hence why it is all np._NoValue)


So you could do things like


```
>>> def my_call(a, b='bob'):
...     print(a, b)
...
... my_call(a=1, b=USE_DEFAULT)
(1, 'bob')
````


I think that would be very helpful for Matplotlib where we have the rcparams to control the defaults all the way at the bottom, but if you want to still have a place holder



```
def highlevel(x, y, color=USE_DEFAULT): 
    low_level(x, y, color=color)
```

```
def f1(a=USE_DEFAULT):
    f2(a=a)

def f2(a='bob'):
    print(a)
```

```
>>> f1(a=USE_DEAULT)
bob
>>> f1()
bob
```


right, but in side of f1 you can got a is USE_DEFAULT which is a singleton useful for nothing but passing down to the next level


I'm not sure about your point.

```
def f3(a=1):
    assert a is not USE_DEFULT

```
always holds



(and let say in the following that we can use USE_DEFAULT_1, USE_DEFAULT_2 (even if a singleton).
but a caller can still do f3(a=USE_DEFAULT)

```
def f1(a=USE_DEFAULT_1):
    # maybe a == USE_DEFAULT_1
    assert a is not USE_DEFAULT_2
    f2(a=a)

def f2(a='bob'):
    print(a)

f1(a=USE_DEFAULT_2)
```


I guess I am picking on the obvious point that wile USE_DEFAULT will never make it through the call, it may still non-the-less come out the bottom into the function namespace
which is I think what you are saying with _1 and _2 👍


Yes.
but it come down in a function only if a default value is set to USE_DEFAULT.


```
def f5(a):...

f5(c=USE_DEFAULT) # <- expoldes?
```


So you are sure that a USE_DEFAULT never escape the scope in which it is defained.

```
def f6(**kwargs):
   assert 'c' not in kwargs

f6(c=USE_DEFAULTS)
```

```
base = {k: USE_DEFAULT for k in known_keys}; base.update(kwargs);
```


DEFAULT = environ.get('MATPLTLIB_FOO', USE_DEFAULT)


```
def f():
   pass
f(x=USE_DEFAULT) # error or not ? 
```

Should likely be an error, avoid typoes/TypeErrors.
