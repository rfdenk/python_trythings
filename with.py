
class X:
    def __init__(self):
        self.v = 0

    def __enter__(self):
        print("enter x")
        return self

    def __exit__(self, exc_type, ex_val, ex_tb):
        print("leave x")

    def accumulate(self, v):
        self.v += v

with X() as x:
    for n in range(10):
        print(n)
        x.accumulate(n)

print(x.v)

x2 = X()
with x2:
    for n in range(10):
        print(n)
        x2.accumulate(n)

print(x2.v)

with x2:
    for n in range(10):
        print(n)
        x2.accumulate(n)
print(x2.v)