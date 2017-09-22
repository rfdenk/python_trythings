import unittest


def add(*args):
    k = 0
    for v in args:
        k = k + v
    return k


def rangeX(*args, brak=')'):
    if len(args) == 0:
        return None
    if len(args) == 1:
        return rangeX(0, args[0], brak)

    if args[1] < args[0]:
        return None

    if args[1] == args[0] and brak[0] != ']':
        return None

    start = args[0]
    stop = args[1]

    if brak[0] == ')':
        stop = args[1]
    else:
        stop = args[1] + 1

    r = []
    q = start

    while q < stop:
        r = r + [q]
        q = q + 1
    return tuple(r)


class TestThisStuff(unittest.TestCase):

    def testAdd(self):
        self.assertEqual(add(1, 2, 3, 4, 5), 15)

    def testRangeXWithNoParameters(self):
        self.assertIsNone(rangeX())

    def testRangeXWithOneParameter(self):
        r = rangeX(4)
        self.assertEqual(len(r), 4)
        self.assertNotIn(4, r)
        self.assertNotIn(-1, r)
        for n in range(4):
            self.assertEqual(r[n], n)
        self.assertIn(0, r)
        self.assertIn(1, r)
        self.assertIn(2, r)
        self.assertIn(3, r)

    def testRangeXWithTwoParameters(self):
        r = rangeX(3, 7)
        self.assertEqual(len(r), 4)
        self.assertNotIn(2, r)
        self.assertNotIn(7, r)
        for n in range(4):
            self.assertEqual(r[n], 3 + n)
        self.assertIn(3, r)
        self.assertIn(4, r)
        self.assertIn(5, r)
        self.assertIn(6, r)

        r = rangeX(5, 12, brak=']')
        self.assertEqual(len(r), 8)
        self.assertNotIn(4, r)
        self.assertNotIn(13, r)
        for n in range(8):
            self.assertEqual(r[n],5 + n)
        self.assertIn(5, r)
        self.assertIn(6, r)
        self.assertIn(7, r)
        self.assertIn(8, r)
        self.assertIn(9, r)
        self.assertIn(10, r)
        self.assertIn(11, r)
        self.assertIn(12, r)

    def testRangeXWithTwoEqualParameters(self):
        self.assertIsNone(rangeX(3,3))

        r = rangeX(6, 6, brak=']')
        self.assertIsNotNone(r)
        self.assertEqual(len(r), 1)
        self.assertIn(6, r)
        self.assertEqual(r[0], 6)

    def testRangeXWithInvertedParameters(self):
        self.assertIsNone(rangeX(4,3))
        self.assertIsNone(rangeX(5,2, brak=']'))

    def testRangeXWithOneNegativeParameter(self):
        self.assertIsNone(rangeX(-2))
