from typing import List
from pprint import pprint

"""
10.1 Sorted Merge: You are given two sorted arrays, A and B, where A has a large enough buffer at the
end to hold B. Write a method to merge B into A in sorted order.
Hints:#332
"""

def merge_arrays(A: List[int], B: List[int]):
    if len(B) == 0:
        # if there is no B, then there is nothing to add to A
        # no op
        return A
    elif len(A) == len(B):
        # if the arrays are the same length
        # then A has no actual values
        # just return B
        A = B
        return B
    
    write_index: int = len(A) - 1
    # assume buffering is zeros
    a_index: int = max(i for i in range (0, len(A)) if A[i] != 0)
    b_index: int = len(B) - 1

    while a_index >= 0 and b_index >= 0:
        print(f"a_index:{a_index} b_index:{b_index} write_index:{write_index}")
        if a_index >= 0 and b_index >= 0:
            # each has valid index
            if A[a_index] > B[b_index]:
                A[write_index] = A[a_index]
                a_index -= 1
            else:
                A[write_index] = B[b_index]
                b_index -= 1
            
            write_index -= 1

    # 2 cases
    # 1: a_index > 0
        # implied that b_index is no longer valid
        # so we can only append A
        # however if we've exhausted B
        # everything in A was sorted to begin with
        # so the remaining elements of A are all smaller than the following elements
        # so A is now sorted
        # and we can end
    # 2: b_index > 0
        # then this is the only case we need to address

    while b_index >= 0:
        A[write_index] = b_index
        b_index -= 1
        write_index -= 1

    return A

#A = sorted([1,7,4,3,2])
#B = sorted([8,4,5,2,2])
#A.extend([0] * len(B))
#pprint(merge_arrays(A, B))
#pprint(merge_arrays([], []))
#pprint(merge_arrays([0], [1]))
#pprint(merge_arrays([1], []))

"""
10.2 Group Anagrams: Write a method to sort an array of strings so that all the anagrams are next to
each other.
Hints: #717, #182, #263, #342
"""

def sort_strings_as_anagrams(arr: List[str]) -> List[str]:
    pass

