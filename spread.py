
kwargs = {'a': 12, 'b':'abc'}

print(kwargs)

def f2(a=0,b=''):
    print('f2', a, b)

def f(**kwargs):
    for n in kwargs:
        print('f', n, kwargs[n])
    f2(**kwargs)

f(**kwargs)

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