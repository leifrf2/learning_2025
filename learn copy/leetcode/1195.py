from threading import Barrier

class FizzBuzz:
    def __init__(self, n: int):
        self.n = n
        self.barrier = Barrier(4)

    # printFizz() outputs "fizz"
    def fizz(self, printFizz: 'Callable[[], None]') -> None:
        for x in range(1, self.n + 1):
            if not x % 5 == 0 and x % 3 == 0:
                printFizz()
            self.barrier.wait()


    # printBuzz() outputs "buzz"
    def buzz(self, printBuzz: 'Callable[[], None]') -> None:
        for x in range(1, self.n + 1):
            if x % 5 == 0 and not x % 3 == 0:
                printBuzz()
            self.barrier.wait()
        

    # printFizzBuzz() outputs "fizzbuzz"
    def fizzbuzz(self, printFizzBuzz: 'Callable[[], None]') -> None:
        for x in range(1, self.n + 1):
            if x % 5 == 0 and x % 3 == 0:
                printFizzBuzz()
            self.barrier.wait()
            

    # printNumber(x) outputs "x", where x is an integer.
    def number(self, printNumber: 'Callable[[int], None]') -> None:
        for x in range(1, self.n + 1):
            if not x % 5 == 0 and not x % 3 == 0:
                printNumber(x)
            self.barrier.wait()
            
