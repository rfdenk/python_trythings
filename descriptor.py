from weakref import WeakKeyDictionary


class Price(object):
    def __init__(self):
        self.default = 0
        self.values = WeakKeyDictionary()

    def __get__(self, instance, owner):
        return self.values.get(instance, self.default)

    def __set__(self, instance, value):
        if value < 0 or value > 100:
            raise ValueError("Price must be between 0 and 100.")
        self.values[instance] = value

    def __delete__(self, instance):
        del self.values[instance]


class Book:
    price = Price()

    def __init__(self, title, price):
        self.title = title
        self.price = price

    def __str__(self):
        return '{0} - {1}'.format(self.author, self.price)

b = Book('dyi drywall', 12)

print("book price =", b.price, flush=True)

b.price = 33


class MyProperty:
    class AccessError(Exception):
        pass

    def __init__(self, fn_get, fn_set=None, fn_del=None):
        self.fn_get = fn_get
        self.fn_set = fn_set
        self.fn_del = fn_del

    def __get__(self, instance, owner):
        print("Getting", instance)
        return self.fn_get(instance)

    def __set__(self, instance, value):
        print("Setting", instance, value)
        if self.fn_set is None:
            raise MyProperty.AccessError("MAY NOT WRITE")
        return self.fn_set(instance, value)

    def __delete__(self, instance):
        if self.fn_del is None:
            raise MyProperty.AccessError("MAY NOT DELETE")
        return self.fn_del(instance)

    def setmethod(self, fn_set):
        return type(self)(self.fn_get, fn_set, self.fn_del)

    def delmethod(self, fn_del):
        return type(self)(self.fn_get, self.fn_set, fn_del)


class TestMyProp:
    def __init__(self, name):
        self.__x = 0
        self.__name = name

    def __str__(self):
        return self.__name

    @MyProperty
    def x(self):
        return self.__x

    # I think that 'x' is now an object of type "MyProperty", and hence has
    # a function called "setmethod", which we are now using as a decorator!
    # Further, x is now identified as a descriptor, because it inherits from
    # MyProperty, which is a descriptor?

    @x.setmethod
    def x(self, x):
        self.__x = x

    # x = MyProperty(getx,setx)


tmp = TestMyProp('tmp')

print(tmp.x, flush=True)
tmp.x = 33
print(tmp.x, flush=True)

tmp2 = TestMyProp('tmp2')
print(tmp2.x, flush=True)
tmp2.x = 123
print(tmp.x, tmp2.x, flush=True)