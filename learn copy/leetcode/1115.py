"""
The same instance of FooBar will be passed to two different threads:

thread A will call foo(), while
thread B will call bar().
Modify the given program to output "foobar" n times.
"""

import threading

class FooBar:
    def __init__(self, n):
        self.n = n
        self.foo_lock = threading.Semaphore(1)
        self.bar_lock = threading.Semaphore(0)

    def foo(self, printFoo: 'Callable[[], None]') -> None:
        
        for i in range(self.n):
            # printFoo() outputs "foo". Do not change or remove this line.
            self.foo_lock.acquire()
            printFoo()
            self.bar_lock.release()


    def bar(self, printBar: 'Callable[[], None]') -> None:
        
        for i in range(self.n):
            # printBar() outputs "bar". Do not change or remove this line.
            self.bar_lock.acquire()
            printBar()
            self.foo_lock.release()