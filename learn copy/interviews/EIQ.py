from typing import Dict, List

class EIQ:
    """
    given a list of sub-lists which represent connections,
    return the count for the number of times each node connects to each other node

    maybe i've misinterpreted the question. it's about direct connections rather
    than indirect connections.

    if it's for direct connections, then going set by set is the only way
    for direct connections, it's always going to be n^2 algorithm

    in the worst case, each node can be connected to each other node
    that's n*n = n^2 connections
    each connection needs to be counted
    so the algorithm will run in O(n^2) time

    """

    def __init__(self):
        pass

    input_1: List[List[str]] = [['a', 'b', 'c'], ['a'], ['b', 'd']]
    output_1_direct: Dict[str, int] = {
        'a': 2,
        'b': 3,
        'c': 2,
        'd': 1
    }
    output_1_indirect: Dict[str, int] = {
        'a': 3,
        'b': 3,
        'c': 3,
        'd': 3
    }

    @abstractmethod
    def eiqSolve(self):

        # direct version
        map_set: Dict[str, set[str]] = dict()

        for sub_list in self.input_1:
            for element in sub_list:
                if not element in map_set.keys():
                    map_set[element] = set()
                map_set[element] = map_set[element].union(sub_list)

        for key, value in map_set.items():
            print(f"{key}: {len(value) - 1}")

