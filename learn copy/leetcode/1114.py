""""
The same instance of Foo will be passed to three different threads.
Thread A will call first(), thread B will call second(), and thread C will call third().
Design a mechanism and modify the program to ensure that second() is executed after first(), and third() is executed after second().
"""

import threading

class Foo:
    def __init__(self):
        self.first_lock = threading.Semaphore(1)
        self.second_lock = threading.Semaphore(0)
        self.third_lock = threading.Semaphore(0)


    def first(self, printFirst: 'Callable[[], None]') -> None:
        
        # printFirst() outputs "first". Do not change or remove this line.
        self.first_lock.acquire()
        printFirst()
        self.second_lock.release()


    def second(self, printSecond: 'Callable[[], None]') -> None:
        
        # printSecond() outputs "second". Do not change or remove this line.
        self.second_lock.acquire()
        printSecond()
        self.third_lock.release()


    def third(self, printThird: 'Callable[[], None]') -> None:
        
        # printThird() outputs "third". Do not change or remove this line.
        self.third_lock.acquire()
        printThird()