

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


func_a('a', 'b', flush=True, end='[EOL]\r\n', sep='.')
func_b('x', 'y', 'z', end='</msg>', sep='<>')
