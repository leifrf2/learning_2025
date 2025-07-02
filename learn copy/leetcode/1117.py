"""
There are two kinds of threads: oxygen and hydrogen. Your goal is to group these threads to form water molecules.

There is a barrier where each thread has to wait until a complete molecule can be formed.
Hydrogen and oxygen threads will be given releaseHydrogen and releaseOxygen methods respectively, which will allow them to pass the barrier.
These threads should pass the barrier in groups of three, and they must immediately bond with each other to form a water molecule.
You must guarantee that all the threads from one molecule bond before any other threads from the next molecule do.

In other words:

If an oxygen thread arrives at the barrier when no hydrogen threads are present, it must wait for two hydrogen threads.
If a hydrogen thread arrives at the barrier when no other threads are present, it must wait for an oxygen thread and another hydrogen thread.
"""

from threading import Semaphore, Barrier

class H2O:
    def __init__(self):
        print('init')
        self.oxygen_lock = Semaphore(1)
        self.hydrogen_lock = Semaphore(2)
        # !!! remember barriers !!!
        self.molecule_lock = Barrier(3)


    def hydrogen(self, releaseHydrogen: 'Callable[[], None]') -> None:
        print("hydrogen")

        with self.hydrogen_lock:
            self.molecule_lock.wait()

            # releaseHydrogen() outputs "H". Do not change or remove this line.
            releaseHydrogen()


    def oxygen(self, releaseOxygen: 'Callable[[], None]') -> None:
        print("oxygen")

        with self.oxygen_lock:
            self.molecule_lock.wait()

            # releaseOxygen() outputs "O". Do not change or remove this line.
            releaseOxygen()

