import pickle

class ToP:
    bar = 'foo'

    def __init__(self, q):
        self.q = q

    def __str__(self):
        return 'ToP:' + self.q

print(pickle.dumps(ToP))


t = ToP('xyz')
print(pickle.dumps(t))

pickled_t = pickle.dumps(t)

t2 = pickle.loads(pickled_t)

print(t2)

print(t is t2)


class A:
    def __init__(self, a):
        self.a = a

    def __str__(self):
        return "A('" + self.a + "')"

class B:
    def __init__(self, a):
        self.a = A(a)

    def __str__(self):
        return "B(" + str(self.a) + ")"

b = B('eee')

pickled_b = pickle.dumps(b)
print(pickled_b)


b2 = pickle.loads(pickled_b)
print(b)
print(b2)

print(b.a is b2.a)