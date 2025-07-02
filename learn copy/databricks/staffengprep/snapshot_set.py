"""
A HashSet data structure that allows Get/Put operations.
Also, snapshot and iterator to snapshot the state of KV and iterate over only the items in a snapshot.

class SnapshotSet(object):
    def __init__(self):
        pass

    def add(self, e):
        pass

    def remove(self, e):
        pass

    # Returns True/False
    def __contains__(self, e):
        pass

    # Returns Iterator object
    def iterator(self):
        pass
    
#Example:      
ss = SnapshotSet([1, 2, 3])
ss.add(4)
iter1 = ss.iterator()
ss.remove(1)
iter2 = ss.iterator()
ss.add(6)
"""