import unittest


class X:
    def __init__(self):
        self.v = 0

    def __enter__(self):
        # print("enter x")
        return self

    def __exit__(self, exc_type, ex_val, ex_tb):
        pass    # print("leave x")

    def accumulate(self, v):
        self.v += v


# Y is like X, but it resets its accumulation
# at the call to with (inside __enter__).
class Y:
    def __init__(self):
        self.v = 0

    def __enter__(self):
        self.v = 0
        # print("enter Y")
        return self

    def __exit__(self, exc_type, ex_val, ex_tb):
        pass    # print("leave Y")

    def accumulate(self, v):
        self.v += v


class TestWith(unittest.TestCase):

    def test_X_once(self):
        expected = 0
        with X() as x:
            for n in range(10):
                x.accumulate(n)
                expected += n
                self.assertEqual(x.v, expected)

        self.assertEqual(x.v, 45)

    def test_X_twice(self):
        x = X()
        expected = 0
        with x:
            for n in range(10):
                x.accumulate(n)
                expected += n
                self.assertEqual(x.v, expected)

        self.assertEqual(x.v, 45)

        with x:
            for n in range(10):
                x.accumulate(n)
                expected += n
                self.assertEqual(x.v, expected)

        self.assertEqual(x.v, 90)

    def test_Y_twice(self):
        y = Y()
        expected = 0
        with y:
            for n in range(10):
                y.accumulate(n)
                expected += n
                self.assertEqual(y.v, expected)

        self.assertEqual(y.v, 45)

        expected = 0
        with y:
            for n in range(10):
                y.accumulate(n)
                expected += n
                self.assertEqual(y.v, expected)

        self.assertEqual(y.v, 45)


if __name__ == '__main__':
    unittest.main()