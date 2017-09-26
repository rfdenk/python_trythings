

class DoSomething:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("Calling", self.func.__name__, 'with', args, kwargs)
        return self.func(*args, **kwargs)


def func_a(a, b, **kwargs):
    print(a, b, **kwargs)


@DoSomething
def func_b(*args, **kwargs):
    print(*args, **kwargs)


# direct decoration...
func_a = DoSomething(func_a)

print(dir(func_a))
print(dir(DoSomething))
print(callable(func_a))
print(callable(func_b))

func_a('a', 'b', flush=True, end='[EOL]\r\n', sep='.')
func_b('x', 'y', 'z', end='</msg>\r\n', sep='<>')


class NoCall:
    def __init__(self, v):
        self.v = v


nc = NoCall(3)
print(dir(nc))
print(callable(nc))
if callable(nc):
    nc()


