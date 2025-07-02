from typing import Set, List, Tuple
from string import ascii_lowercase

class Node[T]:
    # next should be type Node
    def __init__(self, val: T, next = None):
        self.next = next
        self.val = val
    
    def __str__(self) -> str:
        result: str = ""
        current = self

        while current.next:
            result += f"{current.val}->"
            current = current.next

        result += f"{current.val}"

        return result

    def __eq__(self, other) -> bool:
        if type(other) != type(self):
            return False

        current: Node = self
        while current != None:
            if other == None:
                return False
            elif current.val != other.val:
                return False
            else:
                current = current.next
                other = other.next

        # current is known to be none already
        # other must also be none
        return other == None

def create_linked_list[T](array: List[T]) -> Node[T]:
    if len(array) == 0:
        return None
    
    head: Node = Node[T](array[0])

    current: Node[T] = head
    for val in array[1:]:
        current.next = Node[T](val)
        current = current.next

    return head

"""
Remove Dups! Write code to remove duplicates from an unsorted linked list.
FOLLOW UP
"""
def remove_dups(linked_list: Node) -> None:
    if not linked_list:
        # nothing to do
        return
        
    seen_vals = set([linked_list.val])

    current: Node = linked_list
    while current.next != None:
        if current.next.val in seen_vals:
            current.next = current.next.next
        else:
            seen_vals.add(current.next.val)
            current = current.next

remove_dups_tests: List[Tuple[Node, Node]] = [
    (create_linked_list(t[0]), create_linked_list(t[1])) for t in [
        ([], []),
        ([1], [1]),
        ([1, 1], [1]),
        ([1, 2], [1, 2]),
        (list(range(1,10)), list(range(1,10))),
        (list(range(1,10)) + list(range(1,10)), list(range(1,10))),
        ([1] * 7, [1]),
        (ascii_lowercase[1:10] + ascii_lowercase[5:15], ascii_lowercase[1:15])
    ]
]

def run_remove_dups_tests():
    for input, expected_output in remove_dups_tests:
        print(f"test...")
        print(f"input:{input}")
        remove_dups(input)
        print(f"updated:{input}")
        print(f"expected:{expected_output}")
        print(input==expected_output)
        if not input==expected_output:
            raise Exception("Failed test!")

####

"""
Return Kth to Last: Implement an algorithm to find the kth to last element of a singly linked list.
Hints:#8, #25, #41, #67, #126
"""
def kth_to_last[T](k: int, linked_list: Node[T]) -> T:
    if linked_list == None:
        return None

    current: Node = linked_list
    runner: Node = linked_list

    while k > 0:
        current = current.next
        k -= 1
    
    while current.next != None:
        current = current.next
        runner = runner.next
    
    return runner.val

kth_to_last_tests: List[List] = [
    (create_linked_list(list(range(1,5))), 1, 3),
    (create_linked_list([1]), 0, 1),
    (create_linked_list([1,2,3,4,5]), 2, 3)
]

def run_kth_to_last_tests():
    for entry in kth_to_last_tests:
        input_list, input_k, expected_output = entry[0], entry[1], entry[2]
        print(f"test...")
        print(f"input_list:{input_list}, input_k:{input_k}")
        output = kth_to_last(input_k, input_list)
        print(f"output:{output}")
        print(f"expected:{expected_output}")
        correct = output==expected_output
        if correct:
            print("correct")
        else:
            print("********incorrect********")

#run_kth_to_last_tests()

"""
Delete Middle Node: Implement an algorithm to delete a node in the middle (i.e., any node but
the first and last node, not necessarily the exact middle) of a singly linked list, given only access to
that node.
EXAMPLE
lnput:the node c from the linked list a->b->c->d->e->f
Result: nothing is returned, but the new linked list looks like a->b->d->e->f
"""

## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## 

"""
Partition: Write code to partition a linked list around a value x, such that all nodes less than x come
before all nodes greater than or equal to x. If x is contained within the list, the values of x only need
to be after the elements less than x (see below). The partition element x can appear anywhere in the
"right partition"; it does not need to appear between the left and right partitions.
"""

### don't understand this one

"""
Sum Lists: You have two numbers represented by a linked list, where each node contains a single
digit. The digits are stored in reverse order, such that the 1 's digit is at the head of the list. Write a
function that adds the two numbers and returns the sum as a linked list.
EXAMPLE
Input: (7-> 1 -> 6) + (5 -> 9 -> 2).That is,617 + 295.
Output: 2 -> 1 -> 9. That is, 912.
FOLLOW UP
Suppose the digits are stored in forward order. Repeat the above problem.
EXAMPLE
lnput:(6 -> 1 -> 7) + (2 -> 9 -> 5).That is,617 + 295.
Output: 9 -> 1 -> 2. That is, 912.
"""

def sum_lists(list_1: Node[int], list_2: Node[int]) -> int:
    return

def sum_lists_fwd(list_1: Node[int], list_2: Node[int]) -> int:
    return