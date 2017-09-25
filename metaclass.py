import unittest


class Thing1:

    class Inst1:
        def __init__(self):
            self.__x = 0

        def set(self, x):
            self.__x = x

        def get(self):
            # print("THING 1")
            return self.__x


class Thing2:

    class Inst2:
        def __init__(self):
            self.__x = 1

        def set(self, x):
            self.__x = x + 1

        def get(self):
            # print("THING 2")
            return self.__x


class FancyAttrMetaclass(type):

    @staticmethod
    def __make_getter(name):
        def getter(self):
            return getattr(self, name.upper(), None)

        return getter

    @staticmethod
    def __make_setter(name):
        def setter(self, v):
            return setattr(self, name.upper(), v)

        return setter

    def __new__(mcs, class_name, superclasses, attributes):
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


class TestFancyAttr(unittest.TestCase):

    def testIt(self):
        self.assertFalse(hasattr(Foo, 'bar'))
        self.assertTrue(hasattr(Foo, 'BAR'))

    def testSetterAndGetter(self):
        f = Foo()
        self.assertEqual(f.BAR, 'bip')
        self.assertEqual(f._BAZ, 'dip')
        self.assertEqual(f.getbaz(), 'dip')

        f.setbaz('22')
        self.assertEqual(f._BAZ, '22')
        self.assertEqual(f.getbaz(), '22')


#
#
#  Django has this cool thing where you define some class attributes,
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

    def __init__(self):
        # for each of the Thing1 class attributes, make a Thing1.Inst1 instance attribute.
        for name in self._THINGS1:
            exec('self.' + name + ' = Thing1.Inst1()')


# MyDj inherits from Dj, so it execute Dj.__init__, which makes us some nifty instance attributes.
class MyDj(Dj):

    # these are _class_ attributes!
    first_thing = Thing1()
    second_thing = Thing1()

    def setThing1(self, x):
        self.first_thing.set(x)

    def setThing2(self, x):
        self.second_thing.set(x)


class TestDjangoTrick(unittest.TestCase):

    def testThatThingsAreDistinct(self):
        md1 = MyDj()
        md2 = MyDj()

        self.assertFalse(md1.first_thing is md1.second_thing)
        self.assertFalse(md1.first_thing is md2.first_thing)
        self.assertFalse(md1.first_thing is md2.second_thing)
        self.assertFalse(md2.first_thing is md2.second_thing)

    def testInitialValueOfThings(self):
        md1 = MyDj()
        md2 = MyDj()

        self.assertEqual(md1.first_thing.get(), 0)
        self.assertEqual(md1.second_thing.get(), 0)
        self.assertEqual(md2.first_thing.get(), 0)
        self.assertEqual(md2.second_thing.get(), 0)

    def testThingsAreIsolated(self):
        md1 = MyDj()
        md2 = MyDj()

        md1.setThing1(34)
        self.assertEqual(md1.first_thing.get(), 34)
        self.assertEqual(md1.second_thing.get(), 0)
        self.assertEqual(md2.first_thing.get(), 0)
        self.assertEqual(md2.second_thing.get(), 0)

        md2.second_thing.set(101)       # md2.setThing2(101)
        self.assertEqual(md1.first_thing.get(), 34)
        self.assertEqual(md1.second_thing.get(), 0)
        self.assertEqual(md2.first_thing.get(), 0)
        self.assertEqual(md2.second_thing.get(), 101)

        md1.setThing2(456)
        self.assertEqual(md1.first_thing.get(), 34)
        self.assertEqual(md1.second_thing.get(), 456)
        self.assertEqual(md2.first_thing.get(), 0)
        self.assertEqual(md2.second_thing.get(), 101)

        md2.setThing1(1234)
        self.assertEqual(md1.first_thing.get(), 34)
        self.assertEqual(md1.second_thing.get(), 456)
        self.assertEqual(md2.first_thing.get(), 1234)
        self.assertEqual(md2.second_thing.get(), 101)
