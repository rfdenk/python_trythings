

def initaccum():
    def decorator(func):
        func.x = 0
        return func
    return decorator


@initaccum()
def accum(x):
    accum.x += x
    return accum.x


print(accum(2))
print(accum(3))
print(accum(3))
print(accum(3))
print(accum(3))