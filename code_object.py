import dis


def func_c(a, b):
    # print("my arg names =", func_c.__code__.co_varnames[:func_c.__code__.co_argcount])
    c = a + b
    d = c * 2
    return d + 1


print("dir func_c =", dir(func_c))
print("func_c callable =", callable(func_c))

print("func_c =", func_c.__call__(1, 2))

print("func_c call = ", dir(func_c.__call__))

print("func_c vars", func_c.__code__.co_varnames)
print("func_c args", func_c.__code__.co_varnames[:func_c.__code__.co_argcount])
print(func_c.__code__.co_stacksize)

print("func_c code =", func_c.__code__.co_code)
for b in func_c.__code__.co_code:
    print("%02X" % b)
print("func_c consts =", func_c.__code__.co_consts)
print("func_c varnames =", func_c.__code__.co_varnames)
print("func_c cellvars =", func_c.__code__.co_cellvars)
print("func_c names =", func_c.__code__.co_names)


dis.dis(func_c)

a=6
b=7
#
#
code_str = """
def fff(x, y = 1):
    z = x
    z += y
    z += 1
    return x, y, x + y
    
def swapem(x = 1, y = 2):
    return fff(y, x)
    
x = 1
y = 2
print('sum=', fff(x,y))

"""

co = compile(code_str, '<string>', 'exec')

print(co)
exec(co)

print()
print("code =", co.co_code)
print("consts =", co.co_consts)
print("varnames =", co.co_varnames)
print("cellvars =", co.co_cellvars)
print("names =", co.co_names)

dis.dis(co)

print()
print()
print()

from numbers import Number


def Disassemble(co, indent = ''):
    binary_code = co.co_code
    constants = co.co_consts;
    names = co.co_names
    varnames = co.co_varnames

    nb = 0
    while nb < len(binary_code):
        opcode = binary_code[nb]
        nb += 1
        print('%02X' % opcode, end=':')

        if 0x64 == opcode:
            const_index = binary_code[nb]
            nb += 1
            constant = constants[const_index]
            if hasattr(constant, 'co_code'):
                print(indent + 'PUSH CODE {')
                Disassemble(constant, indent + '  ')
                print('   ' + indent + '}')
            elif isinstance(constant, str):
                print(indent + 'PUSH < CONST \'%s\'' % str(constant))
            elif isinstance(constant, Number):
                print(indent + 'PUSH < CONST #%s' % str(constant))
            elif isinstance(constant, tuple):
                print(indent + 'PUSH < CONST %s' % str(constant))
            else:
                print(indent + 'PUSH < CONST %s (%s)' % (constants[const_index], constants[const_index].__class__))
        elif 0x5A == opcode:
            name_index = binary_code[nb]
            nb += 1
            print(indent + 'POP > NAME %s' % names[name_index])
        elif 0x65 == opcode:
            name_index = binary_code[nb]
            nb += 1
            print(indent + 'PUSH < NAME %s' % names[name_index])
        elif 0x74 == opcode:
            global_index = binary_code[nb]
            nb += 1
            print(indent + 'PUSH < GLOBAL %s' % names[global_index])
        elif 0x17 == opcode:
            dummy = binary_code[nb]
            nb += 1
            print(indent + 'ADD (%d)' % dummy)
        elif 0x14 == opcode:
            dummy = binary_code[nb]
            nb += 1
            print(indent + 'MUL (%d)' % dummy)
        elif 0x37 == opcode:
            dummy = binary_code[nb]
            nb += 1
            print(indent + 'INCREASE (%d)' % dummy)
        elif 0x83 == opcode:
            num_args = binary_code[nb]
            nb += 1
            print(indent + 'CALL WITH %d ARGS' % num_args)
        elif 0x53 == opcode:
            dummy = binary_code[nb]
            nb += 1
            print(indent + 'RETURN (%d)' % dummy)
        elif 0x01 == opcode:
            dummy = binary_code[nb]
            nb += 1
            print(indent + 'POP (%d)' % dummy)
        elif 0x7C == opcode:
            name_index = binary_code[nb]
            nb += 1
            print(indent + 'PUSH < REF %s' % varnames[name_index])
        elif 0x7D == opcode:
            name_index = binary_code[nb]
            nb += 1
            print(indent + 'POP > REF %s' % varnames[name_index])
        elif 0x84 == opcode:
            num_args = binary_code[nb]
            nb += 1
            print(indent + 'MAKE FUNCTION WITH %d DEFAULT ARGS' % num_args)
        elif 0x66 == opcode:
            tuple_size = binary_code[nb]
            nb += 1
            print(indent + 'PUSH < TUPLE OF SIZE %d' % tuple_size)
        else:
            dummy = binary_code[nb]
            nb += 1
            print(indent + '[%02x] %d' % (opcode, dummy))


Disassemble(co)



def xyz(x, y):
    return x, y, x + y

#dis.dis(xyz)

def fffx(x, y=1):
    z = x
    z += 1
    return x, y, x + y


def swapemx(x=1, y=2):
    return fffx(y, x)

#dis.dis(fffx)
