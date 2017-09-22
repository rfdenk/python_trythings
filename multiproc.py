from multiprocessing import Pool, Pipe, cpu_count, Process, Value
import time
import os


def f(x):
    return x*x

def getpid(a):
    time.sleep(1)
    return a + 'PID =' + str(os.getpid())

def recv(p):
    rx = p.recv()
    p.send(str(os.getpid()) + '...' + str(rx))
    return str(os.getpid()) + ':' + str(rx)

def add(a, b, result):
    result.value = a + b


if __name__ == '__main__':
    print("My PID =", os.getpid())
    print("Num CPUs =", cpu_count())
    with Pool(processes=4) as pool:
        print(pool.map(f, range(10)))

        for i in pool.imap_unordered(f, range(10)):
            print(i)

        res = pool.apply_async(f, (20,))
        print(res.get(timeout=5))

        res = pool.apply_async(getpid, ('first',))
        print(res.get(timeout=5))

        res_multi = [pool.apply_async(getpid, ('second',)) for i in range(6)]
        for res in res_multi:
            print(res.get(timeout=5))

        (rx,tx) = Pipe(True)
        receiver = pool.apply_async(recv, (rx,))
        tx.send('abc')
        got = tx.recv()
        print("Got from other process:", str(got))
        print("Other process says:", receiver.get(timeout=3))

        result = Value('i', 0)
        p = Process(target=add, args=(2, 6, result))
        p.start()
        p.join()
        print("Other process say that 2 + 6 =", result.value)