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
x = 1
y = 2
print(x + y)
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