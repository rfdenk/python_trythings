
def add(*args):
    k = 0
    for v in args:
        k = k + v
    return k


def rangeX(*args):
    if len(args) == 0:
        return (0,)
    if len(args) == 1:
        return rangeX(0, args[0])
    r = []
    q = args[0]
    while q < args[1]:
        r = r + [q]
        q = q + 1
    return tuple(r)


print(add(1,2,3,4,5))

print(rangeX())
print(rangeX(4))
print(rangeX(3,7))

for q in rangeX(4,9): print(q)