


class Thing1:

    class Inst1:
        def __init__(self):
            self.x = 0

        def set(self, x):
            self.x = x

        def get(self):
            # print("THING 1")
            return self.x


class Thing2:

    class Inst2:
        def doit(self):
            print("THING 2")


class FancyAttrMetaclass(type):

    @staticmethod
    def __make_getter(name):
        def getter(self):
            return getattr(self, name.upper(), None)

        return getter

    def __make_setter(name):
        def setter(self, v):
            return setattr(self, name.upper(), v)

        return setter

    def __new__(mcs, class_name, superclasses, attributes):
        print("in meta new", flush=True)
        new_attributes = {}

        for name, val in attributes.items():
            if name.startswith('__'):
                # leave this one alone
                new_attributes[name] = val
            else:
                # make this class attribute name upper case
                new_attributes[name.upper()] = val

                if name.startswith('_'):
                    # create a getter and setter for this protected class attribute
                    new_attributes['get' + name[1:]] = FancyAttrMetaclass.__make_getter(name)
                    new_attributes['set' + name[1:]] = FancyAttrMetaclass.__make_setter(name)

        # reuse the type.__new__ method
        me = super().__new__(mcs, class_name, superclasses, new_attributes)
        return me


class Foo(metaclass=FancyAttrMetaclass):

    bar = 'bip'
    _baz = 'dip'


print(hasattr(Foo, 'bar'), flush=True)
# Out: False
print(hasattr(Foo, 'BAR'), flush=True)
# Out: True

f = Foo()
print(f.BAR)
# Out: 'bip'

print(Foo.BAR)

print(dir(f), flush=True)


print("baz:", f._BAZ, "getbaz:", f.getbaz(), flush=True)

f.setbaz('22')
print(f._BAZ, f.getbaz(), flush=True)


print(f.BAR, flush=True)
print(f._BAZ, flush=True)






# Django has this cool thing where you define some class attributes,
# and, when you make a new instance of that class, it has some instance
# attributes of the same name, but of a different but related type.

# This is the metaclass that gets the ball rolling on the cool Django trick

# Note that the PyCharm editor will gripe about all sorts of missing attributes,
# but this code will run.
class DjMetaclass(type):

    def __new__(mcs, class_name, superclasses, attributes):
        new_attributes = {}

        # accumulate a list of Thing1 class attributes.
        things1 = []

        for name, val in attributes.items():
            new_attributes[name] = val

            if isinstance(val, Thing1) and not name.startswith('__'):
                things1.append(name)

        new_attributes['__THINGS1'] = things1

        me = super().__new__(mcs, class_name, superclasses, new_attributes)
        return me

    def __init__(cls, name, bases, namespace):
        # move the THINGS1 into the class object instance
        # confession: I'm not quite sure why this step is required...
        thing1_names = getattr(cls, '__THINGS1', [])
        exec('cls._THINGS1 = ' + repr(thing1_names))
        super().__init__(name, bases, namespace)


# Things that want the cool Django trick should inherit from this class.
class Dj(metaclass=DjMetaclass):

    first_thing = Thing1()
    second_thing = Thing1()

    def __init__(self):
        # for each of the Thing1 class attributes, make a Thing1.Inst1 instance attribute.
        for name in Dj._THINGS1:
            exec('self.' + name + ' = Thing1.Inst1()')


# MyDj inherits from Dj, so it will have instance attributes first_thing and second_thing, both
# of type Thing1.Inst1
class MyDj(Dj):
    def setThing1(self, x):
        self.first_thing.set(x)

    def setThing2(self, x):
        self.second_thing.set(x)


print(dir(Dj))
print(dir(MyDj))

md1 = MyDj()
md2 = MyDj()
print("Same?", md1.first_thing is md2.second_thing)

# big test: if we change the th1 in one MyDj instance,
# I don't want it to affect the other one!
print(md1.first_thing.get(), md1.second_thing.get(), md2.first_thing.get(), md2.second_thing.get())

md1.setThing1(34)
print(md1.first_thing.get(), md1.second_thing.get(), md2.first_thing.get(), md2.second_thing.get())

md2.setThing2(104)
print(md1.first_thing.get(), md1.second_thing.get(), md2.first_thing.get(), md2.second_thing.get())
