# USE_DEFAULT / BK.

Note:

To note confuse this with pep 061 (https://www.python.org/dev/peps/pep-0671/) which is also related to default we likely
want to use another name than USE_DEFAULT. It was suggested the this is also "Unpassable", so we may refer to it as
BlackKnight from monty python and the holly grail


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

what a bout a pos-only wrapper? can it take USE_DEFAULT ? 

Pep 12 template
--- 
PEP: <REQUIRED: pep number>
Title: <REQUIRED: pep title>
Author: <REQUIRED: list of authors' real names and optionally, email addrs>
Sponsor: <real name of sponsor>
PEP-Delegate: <PEP delegate's real name>
Discussions-To: <email address or URL>
Status: <REQUIRED: Draft | Active | Accepted | Provisional | Deferred | Rejected | Withdrawn | Final | Superseded>
Type: <REQUIRED: Standards Track | Informational | Process>
Requires: <pep numbers>
Created: <date created on, in dd-mmm-yyyy format>
Python-Version: <version number>
Post-History: <REQUIRED: dates of postings to python-ideas and/or python-dev, in dd-mmm-yyyy format>
Replaces: <pep number>
Superseded-By: <pep number>
Resolution: <url>


Abstract
========

Function caller often want a way to explicitly call a function with a argument asking the callee to use a default value. 
We suggest the introduction of an ``Unpassable`` singleton, which when present in a call site is not passed to the callee,
leading to the given function using it's default value.


Motivation
==========

In many cases, especially when wrapping lower level API it can be inconvenient to expose lower level function default. 
While some singletons like ``None`` can often be used, they are also valid values to call a function with, and extra
care must be taken when propagating default. Thus you can often see libraries using singletons:


```
# protocol.py
_USE_GLOBAL_DEFAULT = object()
def connect(timeout=_USE_GLOBAL_DEFAULT):
    if timeout is _USE_GLOBAL_DEFAULT:
        timeout = default_timeout
    ...

# request.py

from protocol import _USE_GLOBAL_DEFAULT

def request(url, timeout=_USE_GLOBAL_DEFAULT):
    ...
    connect(timeout=timeout)

```

To avoid importing private objects, or using magics constants, callers can also unpack arguments:


``
DEFAULT = object()

def request(url, timeout=DEFAULT):
    ...

    kwargs = {...}
    if timeout is not DEFAULT:
        kwargs['timeout'] = timeout
    connect(**kwargs)


```

[Clearly explain why the existing language specification is inadequate to address the problem that the PEP solves.]


Rationale
=========

[Describe why particular design decisions were made.]


Specification
=============

[Describe the syntax and semantics of any new language feature.]


Backwards Compatibility
=======================

This proposal is fully backward compatible, and be provided opt-in on a per-function basis by a package on PyPI.

Security Implications
=====================

We don't foresee any security implication with the usage of USE_DEFAULT.


Type System
===========

This may need special consideration for the type system. As USE_DEFAULT will never be passed into a function but is its
own type, it should not be considered a type mismatch. 


Performance Consideration
==========================

This will add an overhead to each function call, we haven't investigate the full performance impact.

How to Teach This
=================

There are two sides of teaching the usage of USE_DEFAULT: from the caller and the callee side. 

We can explain that calling a function with `USE_DEFAULT` as a parameter is equivalent to not passing this parameter.

```
plot(x, y, color=USE_DEFAULT) 
plot(x, y) # is the same.
```

We also expect the `USE_DEFAULT` sentinel to be useful to teach and discover libraries.
For example a tutorial can show the full signature of a function without having to replicate all values. 

```
plt.plot(x, y, 
    scalex=USE_DEFAULT,
    scaley=USE_DEFAULT,
    data=USE_DEFAULT,
    alpha=USE_DEFAULT,
    label=USE_DEFAULT,
    use_order=USE_DEFAULT,
    ...)
```

For intermediate users, we can teach USE_DEFAULT as the same time as kwargs with default values, 
as setting a default value to USE_DEFAULT is the only time where a function can get it as an input value.


Reference Implementation
========================

[Link to any existing implementation and details about its state, e.g. proof-of-concept.]


Rejected Ideas
==============

[Why certain ideas that were brought while discussing this PEP were not ultimately pursued.]


Open Issues
===========

[Any points that are still being decided/discussed.]


References
==========

[A collection of URLs used as references through the PEP.]


Copyright
=========

This document is placed in the public domain or under the
CC0-1.0-Universal license, whichever is more permissive.



..
    Local Variables:
    mode: indented-text
    indent-tabs-mode: nil
    sentence-end-double-space: t
    fill-column: 70
    coding: utf-8
    End:


