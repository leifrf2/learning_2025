# start: 4:11PM
# end: 4:51PM

from pprint import pprint
from typing import List, Set, Tuple

# write an algorithm to detect if there are cycles in a spreadsheet

# example:
# cycle between B1 and B2
spreadsheet: List[List[str]] = [
    ["A2", "B2", ""],
    ["A3", "B1", ""],
    ["",   "",   ""]
]

# understanding the problem
"""
Q: a cell can only be empty or contain another cell reference?
A: yes

Q: how big a spreadsheet? to start, can we constrain it to up to 25 columns (Z)?
A: yes

okay, what do we need to find a cycle.
If we take this outside of the spreadseheet scenario and just treat it like a graph
then we'd use a visited set and keep progressing along the chain
if we hit an element we've already visited, there's a cycle

what time complexity should we have here?
if we're traversing and find a cycle, then exit immediately
at most, a cycle could include the entire spreadsheet
so in that case, it could be N

what if there isn't a cycle?
if half the spreadsheet is one chain
and the other half is cells which point to the start of that chain
then that's n cells for which we're doing (n/2) chain searches -> O(n^2)

but if we've done a visited pass for a cell and found that it's not in a cycle,
then we know that as soon as we touch it again in the future, that there isn't a cycle down that path
so we should be able to do this by only touching each cell once
which is O(n) time

Okay, that sounds like a good approach to implement

Next:
What are good test cases here?
- size 0 spreadsheet
- size 1 spreadsheet
- 0 references spreadsheet
- cycle with a few cells in sheet
- cycle with all cells in sheet
- no cycle with all cells populated
- no cycle with some cells populated
- big sheet
- small sheet
"""

def cell_to_index(cell_str: str) -> Tuple[int, int]:
    if len(cell_str) < 2:
        raise ValueError(f"invalid spreadsheet cell representation: {cell_str}")

    column_char = cell_str[0]
    if not column_char.isalpha():
        raise ValueError(f"invalid spreadsheet cell representation: {cell_str}")
    
    row_str = cell_str[1:]
    if not row_str.isnumeric():
        raise ValueError(f"invalid spreadsheet cell representation: {cell_str}")

    return (
        int(row_str) - 1,
        ord(column_char) - ord("A"),
        )

def cell_is_empty(cell_str: str) -> bool:
    return cell_str == ""

def spreasheet_has_cycle(spreadsheet: List[List[str]]) -> bool:

    overall_visited: Set[str] = set()

    for i, row in enumerate(spreadsheet):
        for j, val in enumerate(row):
            if cell_is_empty(val):
                # this cell isn't a reference, so no cycle
                continue
            else:
                # there is a reference, so this could have a cycle
                current_cell: str = val
                visited: Set[str] = set()

                while not cell_is_empty(current_cell):
                    if current_cell in visited:
                        # hit a cycle
                        return True
                    else:
                        visited.add(current_cell)
                        index: Tuple[int, int] = cell_to_index(current_cell)
                        current_cell: str = spreadsheet[index[0]][index[1]]

                # checked through all cells in this chain and a cycle wasn't found
                # so they're all clean and we don't need to visit them again
                overall_visited.union(visited)

                # if the i-jth cell is empty, then we won't go into the loop
                # and the i-jth cell won't be in the visited set, so it isn't added above
                # similarly, the first empty cell hit in the loop will not be added
                # to the visited set
                # so it needs to be added separately
                overall_visited.add(current_cell)

    # processed entire spreadsheet and no cycle was found
    return False

# (spreadsheet, expected_result) 
test_cases: List[Tuple[List[List[int]], bool]] = [
    (
        [
            ["A2", "B2", ""],
            ["A3", "B1", ""],
            ["",   "",   ""]
        ],
        True
    ),
    (
        [
            ["A2", "B2", ""],
            ["A3", "C1", ""],
            ["",   "",   ""]
        ],
        False
    ),
    (
        [[]],
        False
    ),
    (
        [["A1"]],
        True
    ),
    (
        [[""]],
        False
    ),
    (
        [
            ["A2", "B2", "C2"],
            ["A3", "B3", "C3"],
            ["B1", "C1",  ""]
        ],
        False
    ),
    (
        [
            ["A2", "B2", "C2"],
            ["A3", "B3", "C3"],
            ["B1", "C1",  "A1"]
        ],
        True
    ),
    (
        [
            ["", ""],
            ["", "B2"]
        ],
        True
    )
]

for i, (spreadsheet, expected) in enumerate(test_cases):
    print(f"running test case {i}. Expected {expected}:")
    pprint(spreadsheet)

    actual = spreasheet_has_cycle(spreadsheet)
    print(f"actual: {actual}")
    assert actual == expected

