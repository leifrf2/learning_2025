from typing import List, Dict, Tuple, Set
from pprint import pprint

# recursion and dynamic programming

def fibonacci(i: int) -> int:
    if i < 0:
        return -1
    elif i == 0:
        return 0
    elif i == 1:
        return 1
    elif i == 2:
        return 1
    
    buffer: List[int] = [1, 2]
    for _ in range(3, i + 1):
        buffer.append(buffer[0] + buffer[1])
        buffer.pop(0)

    return buffer[-1]

# 8.1
"""Triple Step: A child is running up a staircase with n steps and can hop either 1 step, 2 steps, or 3
steps at a time. Implement a method to count how many possible ways the child can run up the
stairs.
"""
triple_step_memo: Dict[int, int] = {}

def triple_step(n: int) -> int:
    # there are 3 ways we can get to the nth step
    if n < 1:
        return 0
    elif n == 1:
        return 1
    elif n in triple_step_memo.keys():
        return triple_step_memo[n]
    else:
        solution = triple_step(n - 1) + triple_step(n - 2) + triple_step(n - 3)
        triple_step_memo[n] = solution
        return solution

#8.2
"""
Robot in a Grid: Imagine a robot sitting on the upper left corner of grid with r rows and c columns.
The robot can only move in two directions, right and down, but certain cells are "off limits" such that
the robot cannot step on them. Design an algorithm to find a path for the robot from the top left to
the bottom right.
"""
HOLE = 3
ROBOT = 2
GOAL = 1
def robot_travel(rows: int, cols: int, grid: List[List[int]]) -> List[Tuple[int, int]]:

    travel_history: Dict[Tuple[int, int], bool] = {
        (0, 0): True
    }

    def cell_is_valid(cell: Tuple[int, int]) -> bool:
        return cell[0] >= 0 and cell[0] < rows and cell[1] >= 0 and cell[1] < cols and grid[cell[0]][cell[1]] != HOLE

    def sub_robot_travel(destination: Tuple[int, int]) -> List[Tuple[int, int]]:
        if destination == (0, 0):
            return [destination]
        elif destination in travel_history.keys():
            return [travel_history[destination]]
        else:
            cell_up: Tuple[int, int] = (destination[0] - 1, destination[1])
            cell_left: Tuple[int, int] = (destination[0], destination[1] - 1)

            # if each cell is valid, explore it
            if cell_is_valid(cell_up):
                cell_up_path = sub_robot_travel(cell_up)
            else:
                cell_up_path = None
            
            if cell_is_valid(cell_left):
                cell_left_path = sub_robot_travel(cell_left)
            else:
                cell_left_path = None

            if cell_left_path != None:
                return cell_left_path + [destination]
            elif cell_up_path != None:
                return cell_up_path + [destination]
            else: 
                return None

    # the goal is to reach the robot at [r-1, c-1]
    return sub_robot_travel((rows-1, cols-1))

robot_travel_tests: List[List[List[int]]] = [
    [[0, 0],
     [0, 0]],
    [[0, 0, 0],
     [0, HOLE, 0],
     [0, HOLE, 0]],
    [[0, 0, 0],
     [HOLE, HOLE, HOLE],
     [0, 0, 0]],
]

#for test in robot_travel_tests:
#    print(robot_travel(len(test), len(test[0]), test))

#8.3
"""
Magic Index: A magic index in an array A [ 0 ••• n -1] is defined to be an index such that A[ i] =
i. Given a sorted array of distinct integers, write a method to find a magic index, if one exists, in
array A.
FOLLOW UP
What if the values are not distinct?
"""
def magic_index(input: List[int]) -> int:

    # one way is to just linear search
    # but that's slow
    # the array is sorted, so we can do a binary search at minimum
    # *** distinct integers ***
    # this means that they can only go down so fast


    # if input[i] == i, return

    # when do we go right?

    if len(input) == 0:
        return -1
    elif len(input) == 1:
        return 0 if input[0] == 0 else -1

    lower: int = 0
    upper: int = len(input) - 1
    mid: int = int(len(input) / 2)
    while lower != upper:
        print(f"lower:{lower} mid:{mid} upper:{upper} val:{input[mid]}")
        if input[mid] == mid:
            return mid
        elif input[mid] < mid:
            # e.g. input[mid] = 15, mid = 5
            # there could still be one to the left
            # the values can be negative
            lower = mid
            mid = int(mid + (upper - mid) / 2)
        elif input[mid] > mid:
            # it could be to the left
            upper = mid
            mid = int(mid - (mid - lower) / 2)
        else:
            raise Exception("Impossible case")

        # input[mid] > mid
        # e.g. input[mid] = 8, mid = 5
        # there will never be a magic number here
        # beceause the array value will be increasing by 1+ each time
        # and the index will be increasing by 1 each time
        # so the index will never come up to the array value

    return -1

magic_index_test_arrays: List[Tuple[List[int], int]] = [
    ([0, 5, 8, 10, 15], 0),
    ([-10, -5, 2, 8, 10, 30], 2),
    ([0], 0),
    ([], -1)
]

#for arr, expected in magic_index_test_arrays:
#    print(f"{arr} -> {magic_index(arr)==expected}")

# it is a set coming in, we just skipped the step of casting it to a list
# a set is guaranteed to have all unique items, so any combination of elements
# within the list is also guaranteed to be unique
# all subsets are requested, which is 2^n anyway
def power_set[T](a: List[T]) -> List[List[T]]:
    if len(a) == 0:
        return list()
    elif len(a) == 1:
        return [a, []]
    else:
        # 2 or more elements
        next_element = a[0]
        sub_list_take: List[T] = [sub_list + [next_element] for sub_list in power_set(a[1:])]
        sub_list_dont_take: List[T] = [sub_list for sub_list in power_set(a[1:])]

    sub_list_take.extend(sub_list_dont_take)
    return sub_list_take

#pprint(power_set(list(range(5))))


#8.6
"""
8.6 Towers of Hanoi: In the classic problem of the Towers of Hanoi, you have 3 towers and N disks of
different sizes which can slide onto any tower. The puzzle starts with disks sorted in ascending order
of size from top to bottom (i.e., each disk sits on top of an even larger one). You have the following
constraints:
(1) Only one disk can be moved at a time.
(2) A disk is slid off the top of one tower onto another tower.
(3) A disk cannot be placed on top of a smaller disk.
Write a program to move the disks from the first tower to the last using stacks.
"""

# https://runestone.academy/ns/books/published/pythonds/Recursion/TowerofHanoi.html
# *** I don't fully understand this one
def moveTower(height,fromPole, toPole, withPole):
    if height >= 1:
        moveTower(height-1,fromPole,withPole,toPole)
        moveDisk(fromPole,toPole)
        moveTower(height-1,withPole,toPole,fromPole)

def moveDisk(fp,tp):
    print("moving disk from",fp,"to",tp)

#8.9
"""
Parens: Implement an algorithm to print all valid (e.g., properly opened and closed) combinations
of n pairs of parentheses.
"""
def generate_valid_parens_sets(n: int) -> Set[str]:
    if n <= 0:
        return [""]
    elif n == 1:
        return ["()"]
    else:
        n_1: Set[str] = generate_valid_parens_sets(n-1)
        set_1 = ["(" + s + ")" for s in n_1]
        set_2 = ["()" + s for s in n_1]
        set_3 = [s + "()" for s in n_1]

        return set(set_1 + set_2 + set_3)

def generate_valid_parens_rec(left: int, right: int) -> List[str]:
    # print(f"left:{left} right:{right}")
    if left == 0 and right == 0:
        return [""]

    if left == 1 and right == 1:
        return ["()"]

    if left == 0 and right > 0:
        return [")" + x for x in generate_valid_parens_rec(left, right - 1)]

    if left > right:
        # we can never have more rights deployed than lefts
        # because a close must be preceeded by an open
        raise Exception("This is impossible")

    if left == right:
        # they're not both zero
        # so they're both positive
        # but we can't add a right
        return ["(" + x for x in generate_valid_parens_rec(left - 1, right)]
    
    if left < right:
        result_list = ["(" + x  for x in generate_valid_parens_rec(left - 1, right)]
        result_list.extend([")" + x for x in generate_valid_parens_rec(left, right - 1)])
        return result_list

def generate_valid_parens(n: int) -> List[str]:
    if n == 0:
        return []
    elif n == 1:
        return "()"
    else:
        return generate_valid_parens_rec(n, n)


#8.10
"""
Paint Fill: Implement the "paint fill" function that one might see on many image editing programs.
That is, given a screen (represented by a two-dimensional array of colors), a point, and a new color,
fill in the surrounding area until the color changes from the original color.
"""

# skip because it's annoying to set up
# clear how to solve

#8.11
"""
Coins: Given an infinite number of quarters (25 cents), dimes (10 cents), nickels (5 cents), and
pennies (1 cent), write code to calculate the number of ways of representing n cents.
"""

# return is number of ways
def calculate_coins(n: int) -> int:
    # the order doesn't matter
    # so we could do this with sets
    # but that's a cop out

    # how do we solve this without caring about order?

    # take all the 25s first
    # then al the 10s
    # then all the 5s
    # then all the 1s

    def calculate_coins(n: int, descending_coin_options: List[int]) -> int:
        if n == 0:
            return 1
        elif len(descending_coin_options) == 0:
            # implicitly, n is greater than 0
            # and there are no coins left
            # so there are no matches
            return 0
        
        accumulator: int = 0

        # this way, we always take coins in the same order
        # and we ensure there is a unique # of each coin taken at each iteration
        current_coin: int = descending_coin_options[0]

        n_decrementor: int = n
        while n_decrementor >= 0:
            accumulator += calculate_coins(n_decrementor, descending_coin_options[1:])
            n_decrementor -= current_coin
            
        print(f"{n} {descending_coin_options} {accumulator}")
        return accumulator


    return calculate_coins(n, sorted([25, 10, 5, 1], reverse=True))

#8.13
"""
Stack of Boxes: You have a stack of n boxes, with widths wi
, heights hi
, and depths di
. The boxes
cannot be rotated and can only be stacked on top of one another if each box in the stack is strictly
larger than the box above it in width, height, and depth. Implement a method to compute the
height of the tallest possible stack. The height of a stack is the sum of the heights of each box.
"""

# we can't do this the greedy way because there isn't necessarily a box that we'd always take
# but we can do by "what if we took this box?"

class Box:
    def __init__(self,
                 height,
                 depth,
                 width):
        self.height = height
        self.depth = depth
        self.width = width

    def can_stack_on(self, other_box) -> bool:
        return self.height < other_box.height \
        and self.width < other_box.width \
        and self.depth < other_box.depth

    def __key(self):
        return (self.height, self.depth, self.width)

    def __hash__(self):
        return hash(self.__key())        

# but what is the memo?
# i think in on one hand it should be a combination of boxes

box_memo: Dict[Box, int] = dict()

def stack_boxes(boxes: List[Box]) -> int:

    if len(boxes) == 0:
        return 0
    boxes.sort(key=lambda b: b.height, reverse=True)

    stack_memo: Dict[int, int] = dict()

    def stack_boxes_sub(bottom_index: int) -> int:
        if bottom_index in stack_memo.keys():
            return stack_memo[bottom_index]
        
        #else, compute it
        if bottom_index == -1:
            # in the first pass, we need to start with each box as bottom
            max_stack_height = max(
                stack_boxes_sub(next_box_index) for next_box_index \
                    in range(bottom_index+1, len(boxes))
            )
        else:
            # this pass only triggers when we already have a bottom box
            current_bottom: Box = boxes[bottom_index]

            max_stack_height = current_bottom.height + max(
                [stack_boxes_sub(next_box_index) \
                    for next_box_index \
                        in range(bottom_index+1, len(boxes)) \
                if boxes[next_box_index].can_stack_on(current_bottom)] + [0]
            )

        stack_memo[bottom_index] = max_stack_height

        return max_stack_height

    return stack_boxes_sub(-1)

box_tests: List[List[Box]] =[
    [Box(1,1,1), Box(2,2,2), Box(3,3,3)],
    #[Box(1,1,1)],
    #[]
]

for test in box_tests:
    pprint(stack_boxes(test))
