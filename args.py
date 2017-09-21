
def add(*args):
    k = 0
    for v in args:
        k = k + v
    return k


def rangeX(*args, brak=')'):
    if len(args) == 0:
        return None
    if len(args) == 1:
        return rangeX(0, args[0], brak)

    start = args[0]
    stop = args[1]

    if brak[0] == ')':
        stop = args[1]
    else:
        stop = args[1] + 1

    r = []
    q = start

    while q < stop:
        r = r + [q]
        q = q + 1
    return tuple(r)


print(add(1,2,3,4,5))

print(rangeX())
print(rangeX(4))
print(rangeX(3,7))

for q in rangeX(4, 9, brak=']'): print(q, end=',')
