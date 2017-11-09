

class Mixin1:
    def show(self):
        print(self.val)


class Derived(Mixin1):
    def __init__(self,v):
        self.val = v


def mixit():
    d = Derived(3)
    d.show();


if __name__ == "__main__":
    mixit()
