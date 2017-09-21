
def memoize(f):
    memo = {}

    def helper(*args, **kwargs):
        key = (args, frozenset(kwargs.items()))
        if key not in memo:
            print('Adding ' + str(key) + ' to memo')
            memo[key] = f(*args, **kwargs)
        return memo[key]
    return helper


class Memoize:
    def __init__(self, fn):
        self.fn = fn
        self.memo = {}

    def __call__(self, *args):
        if args not in self.memo:
            print("Adding " + str(args) + " to Memoize")
            self.memo[args] = self.fn(*args)
        return self.memo[args]


@memoize
def fib(n, **kwargs):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1, **kwargs) + fib(n-2, **kwargs)


@Memoize
def add(a, b):
    return a + b


print(fib(10, j=1, k=4))
print()
print(fib(12, k=4, j=1))

print()
print()
print(str(add(1, 2)))
print(str(add(2, 3)))
print(str(add(1, 2)))
