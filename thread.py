
import time
from threading import Thread, Event, Lock, enumerate as enum_threads, Timer, current_thread, Barrier, Condition
"""
class Response:
    def __init__(self):
        self.lock = Lock()
        self.x = 0

    def set(self, x):
        with self.lock:
            self.x = x

    def get(self):
        with self.lock:
            return self.x


def slowfunc(ev, resp):
    ev.set()
    print(current_thread().name, "connecting", flush=True)
    time.sleep(2)
    print(current_thread().name, "querying", flush=True)
    time.sleep(2)
    print(current_thread().name, "receiving", flush=True)
    time.sleep(2)
    print(current_thread().name, "done!")
    resp.set(122)


e = Event()
resp = Response()
th = Thread(target=slowfunc, name='SlowFunc', args=(e, resp))
th.start()

e.wait()
print(enum_threads(), flush=True)

print("joining!", flush=True)
while True:
    th.join(1)
    print(resp.get())
    if not th.is_alive(): break


print("joined!", flush=True)


resp = Response()
th2 = Thread(target=slowfunc, name='SlowFunc2', args=(e, resp))
t = Timer(4.0, th2.start)
t.start()


class AsyncQuery:
    def __init__(self, resp):
        self.thread = Thread(target=AsyncQuery.query, name='async class', args=(self, resp,))

    def start(self):
        self.thread.start()

    @staticmethod
    def query(instance, resp):
        instance.__query(resp)

    def __query(self, resp):

        print(current_thread().name, "connecting", flush=True)
        time.sleep(2)
        print(current_thread().name, "querying", flush=True)
        time.sleep(2)
        print(current_thread().name, "receiving", flush=True)
        time.sleep(2)
        print(current_thread().name, "done!")
        resp.set(404)

    def wait(self):
        print(current_thread().name, "waiting")
        self.thread.join()

r = Response()
async = AsyncQuery(r)
async.start()
async.wait()
print('a response=', r.get())

"""

"""
class Communicator:
    def __init__(self):
        self.x = None
        self.lock = Lock()

    def send(self, x):
        with self.lock:
            self.x = x

    def receive(self):
        with self.lock:
            return self.x


def thread_using_barrier(barrier, channel):
    print(current_thread().name, 'waiting for sender')
    barrier.wait()
    x = channel.receive()
    print(current_thread().name, "got", x)
    time.sleep(3)
    print(current_thread().name, 'done')


barrier = Barrier(2)
channel = Communicator()

thb = Thread(target=thread_using_barrier, name='THB', args=(barrier, channel))
thb.start()

time.sleep(4)
channel.send('abc')
barrier.wait()

"""


class Chx(Condition):
    def __init__(self):
        self.x = 0
        super().__init__()

    def send(self, x):
        self.x = x
        self.notify()

    def get(self):
        return self.x


def producer_with_cv(cv):
    """
    for n in range(2):
        time.sleep(2)
        with cv:
            cv.send(n)
            print(current_thread().name, "produced", flush=True)
    """
    for n in range(2):
        time.sleep(2)
        cv.acquire()
        cv.send(n+1)
        print(current_thread().name, "produced", flush=True)
        cv.release()

def consumer_with_cv(cv):
    """
    with cv:
        cv.wait()
        print(current_thread().name, "consumed", cv.get(), flush=True)
    """
    cv.acquire()
    cv.wait()
    print(current_thread().name, "consumed", cv.get(), flush=True)
    cv.release()

cv = Chx()
thcv = Thread(target=consumer_with_cv, name="THCV", args=(cv,))
thcv.start()
thcv2 = Thread(target=consumer_with_cv, name="THCV2", args=(cv,))
thcv2.start()
thpv = Thread(target=producer_with_cv, name="THPV", args=(cv,))
thpv.start()
