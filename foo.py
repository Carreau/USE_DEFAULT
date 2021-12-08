from unpassable import Unpassable, ignore_unpassable

@ignore_unpassable
def foo(x,y,z='z_default',d='d_default'):
    print(f"got        {x!r}, {y!r}, {z!r}, {d!r}")

@ignore_unpassable
def bar(val=Unpassable):
    assert val is Unpassable
    foo(1, 2, d=val)



print("expecting", (1, 2, 'z_default', 3))
foo(1, 2, Unpassable, 3)

print("expecting", (1, 2, 'z_default', 'd_default'))
bar()


print("expecting", TypeError)
try:
    foo(1, Unpassable, 3, 4)
except TypeError as e:
    print('Got      ', type(e))


print("expecting", (1, 'bob'))

@ignore_unpassable
def my_call(a, b='bob'):
    print(a, b)

my_call(a=1, b=Unpassable)
