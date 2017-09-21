
def generate():
    yield('a')
    yield('b')
    yield('c')


for v in generate():
    print(v)


def gen2():
    # x = yield(1)
    x = 0
    while True:
        if x < 100:
            x = yield(x+1)
        else:
            break;


print()
print()

g2 = gen2()
g = next(g2)
while True:
    try:
        print(g)
        g = g2.send(g)
    except StopIteration:
        break


def permutations(items):
    print("Permuting", items)
    n = len(items)
    if n == 0:
        yield []
    else:
        for i in range(len(items)):
            for cc in permutations(items[:i]+items[i+1:]):
                yield [items[i]]+cc


for p in permutations(['r','e']): print(''.join(p))
# for p in permutations(list("game")): print(''.join(p) + ", ", end="")


from functools import wraps

def prepare_generator(func):
    @wraps(func)
    def prep(*args, **kwargs):
        g = func(*args, **kwargs)
        next(g)
        return g
    return prep


@prepare_generator
def running_average(initial_average=None, initial_count=None):
    total = (initial_average * initial_count) if initial_average is not None and initial_count is not None else 0.0
    counter = initial_count if initial_count is not None else 0
    average = (initial_average if initial_count is not None else None)
    while True:
        print("about to yield", average)
        term = yield(average)
        total += term
        counter += 1
        average = total / counter

print()
print()
ra = running_average()
for value in [7, 13, 17, 231, 12, 8, 3]:
    out_str = "sent: {val:3d}, new average: {avg:6.2f}"
    print(out_str.format(val=value, avg=ra.send(value)))

print()
print()

ra = running_average(initial_average=10, initial_count=2)
for value in [17, 231, 12, 8, 3]:
    out_str = "sent: {val:3d}, new average: {avg:6.2f}"
    print(out_str.format(val=value, avg=ra.send(value)))


