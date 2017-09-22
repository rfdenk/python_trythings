import unittest

memoize_count = 0


def memoize(f):
    memo = {}

    def helper(*args, **kwargs):
        key = (args, frozenset(kwargs.items()))
        if key not in memo:
            # print('Adding ' + str(key) + ' to memo')
            memo[key] = f(*args, **kwargs)
            helper.call_count += 1      # keep track of how many times we invoke the actual function
        return memo[key]

    helper.call_count = 0
    return helper


class Memoize:
    def __init__(self, fn):
        self.fn = fn
        self.call_count = 0
        self.memo = {}

    def __call__(self, *args):
        if args not in self.memo:
            # print("Adding " + str(args) + " to Memoize")
            self.memo[args] = self.fn(*args)
            self.call_count += 1        # keep track of how many times we invoke the actual function
        return self.memo[args]


@memoize
def fib(n, **kwargs):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1, **kwargs) + fib(n-2, **kwargs)


@memoize
def fibX(n, **kwargs):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibX(n-1, **kwargs) + fibX(n-2, **kwargs)


@Memoize
def fib2(n, **kwargs):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib2(n-1, **kwargs) + fib2(n-2, **kwargs)


@Memoize
def add(a, b):
    return a + b


class TestMemoize(unittest.TestCase):

    def testMemoizeWithFunc(self):
        self.assertEqual(fib(10, j=1, k=4), 55)
        self.assertEqual(fib(12, k=4, j=1), 144)
        self.assertEqual(fib.call_count, 13)        # the kwargs are the same, so we can use the memo
        self.assertEqual(fib(10, j=2, q=4), 55)     # same computation, but the kwargs differ, so we can't use the memo
        self.assertEqual(fib.call_count, 24)        # the kwargs changed, so we augmented the memo with acutal calls

        # make sure that the functions have separate call_counts
        self.assertEqual(fibX.call_count, 0)
        self.assertEqual(fibX(6), 8)
        self.assertEqual(fib.call_count, 24)
        self.assertEqual(fibX.call_count, 7)

    def testMemoizeWithClass(self):
        self.assertEqual(fib2(10), 55)
        self.assertEqual(fib2.call_count, 11)
        self.assertEqual(fib2(12), 144)
        self.assertEqual(fib2.call_count, 13)

        # make sure that other functions counts have not been affected
        self.assertEqual(add.call_count, 0)
        self.assertEqual(add(1,2), 3)
        self.assertEqual(add.call_count, 1)
        self.assertEqual(fib2.call_count, 13)

        self.assertEqual(add(2,3), 5)
        self.assertEqual(add.call_count, 2)

        self.assertEqual(add(1,2), 3)
        self.assertEqual(add.call_count, 2)


def enabled(func):
    return func

def disabled(func):
    def nothing(*args, **kwargs):
        pass
    return nothing

state = disabled

@state
def dbg_func(a):
    print(a)

dbg_func('123')
