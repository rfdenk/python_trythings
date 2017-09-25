
import unittest
from copy import deepcopy


def gen1():
    yield('a')
    yield('b')
    yield('c')


def gen2():
    x = 0
    while True:
        if x == 0:
            x = yield(1)
        elif x < 16:
            x = yield(x*2)
        else:
            break;


class TestGenerators(unittest.TestCase):
    def testGen1(self):
        expected = ('a', 'b', 'c')
        n = 0
        for v in gen1():
            self.assertEqual(v, expected[n])
            n += 1

    def testGen2(self):
        g2 = gen2()
        g = next(g2)
        n = 1
        while True:
            try:
                self.assertEqual(n, g)
                g = g2.send(g)
                n = n * 2
            except StopIteration:
                self.assertEqual(g, 16)
                break


def permutations(items):
    n = len(items)
    if n == 0:
        yield []
    else:
        for i in range(len(items)):
            for cc in permutations(items[:i]+items[i+1:]):
                yield [items[i]]+cc


class TestPermuter(unittest.TestCase):
    def testPermuter(self):
        perms = []
        for p in permutations(['r', 'e', 'd']):
            perms.append(''.join(p))
        self.assertEqual(perms, ['red', 'rde', 'erd', 'edr', 'dre', 'der'])


# for p in permutations(list("game")): print(''.join(p) + ", ", end="")


from functools import wraps


def prepare_generator(func):
    @wraps(func)
    def prep(*args, **kwargs):
        g = func(*args, **kwargs)
        next(g)
        return g
    return prep


@prepare_generator
def running_average(initial_average=None, initial_count=None):
    total = (initial_average * initial_count) if initial_average is not None and initial_count is not None else 0.0
    counter = initial_count if initial_count is not None else 0
    average = (initial_average if initial_count is not None else None)
    while True:
        # print("about to yield", average)
        term = yield(average)
        total += term
        counter += 1
        average = total / counter


class TestRunningAverageGenerator(unittest.TestCase):

    def testRunningAverage(self):
        values = [7, 13, 17, 231, 12, 8, 3]
        averages = ['  7.00', ' 10.00', ' 12.33', ' 67.00', ' 56.00', ' 48.00', ' 41.57']
        ra = running_average()
        n = 0
        for value in values:
            self.assertEqual('{avg:6.2f}'.format(avg=ra.send(value)), averages[n])
            n += 1

    def testRunningAverageWithInitialState(self):
        values = [17, 231, 12, 8, 3]
        averages = [' 12.33', ' 67.00', ' 56.00', ' 48.00', ' 41.57']
        ra2 = running_average(initial_average=10, initial_count=2)
        n = 0
        for value in values:
            self.assertEqual('{avg:6.2f}'.format(avg=ra2.send(value)), averages[n])
            n += 1


def prepare_generator2(*outer_args, **outer_kwargs):
    base_args = outer_args[:]
    base_kwargs = deepcopy(outer_kwargs)
    def prep(func):
        def inner(*args, **kwargs):
            new_args = base_args + args
            new_kwargs = base_kwargs;
            new_kwargs.update(kwargs)
            g = func(*new_args, **new_kwargs)
            next(g)
            return g
        return inner
    return prep


@prepare_generator2(initial_average=10, initial_count=2)
def running_average2(initial_average=None, initial_count=None):
    total = (initial_average * initial_count) if initial_average is not None and initial_count is not None else 0.0
    counter = initial_count if initial_count is not None else 0
    average = (initial_average if initial_count is not None else None)
    while True:
        # print("about to yield", average)
        term = yield(average)
        total += term
        counter += 1
        average = total / counter


@prepare_generator2()
def running_average3(initial_average=None, initial_count=None):
    total = (initial_average * initial_count) if initial_average is not None and initial_count is not None else 0.0
    counter = initial_count if initial_count is not None else 0
    average = (initial_average if initial_count is not None else None)
    while True:
        # print("about to yield", average)
        term = yield(average)
        total += term
        counter += 1
        average = total / counter


class TestRunningAverage2Generator(unittest.TestCase):

    def testRunningAverage2(self):

        values = [17, 231, 12, 8, 3]
        averages = [' 12.33', ' 67.00', ' 56.00', ' 48.00', ' 41.57']
        ra2 = running_average2()
        n = 0
        for value in values:
            self.assertEqual('{avg:6.2f}'.format(avg=ra2.send(value)), averages[n])
            n += 1

    def testRunningAverage3(self):
        values = [7, 13, 17, 231, 12, 8, 3]
        averages = ['  7.00', ' 10.00', ' 12.33', ' 67.00', ' 56.00', ' 48.00', ' 41.57']
        ra = running_average3()
        n = 0
        for value in values:
            self.assertEqual('{avg:6.2f}'.format(avg=ra.send(value)), averages[n])
            n += 1

