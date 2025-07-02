"""
Design a class newString such that the time complexity for insertion, deletion and read is less than o(N).

class NewString:
    def __init__(self):
        self.data = []  # Using a list to store characters (mutable string)

    def read(self, index: int) -> str:
        pass

    def insert(self, c: str, index: int):
       pass

    def delete(self, index: int):
        pass
"""

# read is const for list, dict
    # tree is logn

# insert is technically n time because we need to move indices of everything after
    # dict is const
    # tree is logn

# insert is log n time

# in the examp,e it's always an int index though
# so this can just be a dict or list