import unittest


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


class TestCurrying(unittest.TestCase):

    def test1(self):
        curried_func = curry(func, 1, 2, multiply_by=3)

        # (1 + 2 + 3) * 3 = 18
        self.assertEqual(curried_func(3), 18)

        # (1 + 2 + 4) * 2 = 14
        self.assertEqual(curried_func(4, multiply_by=2), 14)

if __name__ == '__main__':
    unittest.main()