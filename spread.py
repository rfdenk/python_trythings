
kw = {'a': 12, 'b': 'abc'}

print(kw)


def f2(*args, a=0, b='_'):
    print('f2a', args)
    print('f2', a, b)


def f(*args, **kwargs):
    for a in args:
        print('fa', a)
    for n in kwargs:
        print('fkw', n, kwargs[n])
    f2(*args, **kwargs)


f(kw)
f(**kw)

lst = (1, 2, 3)
print("list", lst)


def fl(*args):
    for n in args:
        print('fl', n)


fl(lst)
fl(1, 2, 3)


def fl2(*args):
    print('fl2')
    fl(args)
    fl(*args)


fl2(lst)
fl2(1, 2, 3)
