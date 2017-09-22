import unittest

def initaccum():
    def decorator(func):
        func.x = 0
        return func
    return decorator


@initaccum()
def accum(x):
    accum.x += x
    return accum.x


class TestAccumulator(unittest.TestCase):

    def testIt(self):
        self.assertEqual(accum(2), 2)
        self.assertEqual(accum(3), 5)
        self.assertEqual(accum(3), 8)
        self.assertEqual(accum(3), 11)
        self.assertEqual(accum(3), 14)
        self.assertEqual(accum(6), 20)
