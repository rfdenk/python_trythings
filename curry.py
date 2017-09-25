
def curry(f, *fixed_args, **fixed_kwargs):
    f_args = fixed_args[:]
    f_kwargs = dict(**fixed_kwargs)

    def __curry(*args, **kwargs):
        new_kwargs = f_kwargs
        new_kwargs.update(kwargs)
        new_args = f_args + args
        return f(*new_args, **new_kwargs)
    return __curry


def func(a, b, c, multiply_by=1):
    return (a + b + c) * multiply_by


curried_func = curry(func, 1, 2, multiply_by=3)

print(curried_func(3))
print(curried_func(3, multiply_by=2))
