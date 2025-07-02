"""
You live in San Francisco city and want to minimize your commute time to the Databricks HQ.
Given a 2D matrix of the San Francisco grid and the time as well as cost matrix of all the available transportation modes, 
return the fastest mode of transportation. If there are multiple such modes then return one with the least cost.

Rules:
- The input grid represents the city blocks, so the commuter is only allowed to travel along the horizontal and vertical axes. Diagonal traversal is not permitted.
- The commuter can only move to the neighboring cells with the same transportation mode.

Sample Input:
    2D Grid: Legend:
    |3|3|S|2|X|X| X = Roadblock
    |3|1|1|2|X|2| S = Source
    |3|1|1|2|2|2| D = Destination
    |3|1|1|1|D|3| 1 = Walk, 2 = Bike, 3 = Car, 4 = Train
    |3|3|3|3|3|4|
    |4|4|4|4|4|4|

    Transportation Modes: ["Walk", "Bike", "Car", "Train"]
    Cost Matrix (Dollars/Block): [0, 1, 3, 2]
    Time Matrix (Minutes/Block): [3, 2, 1, 1]
    Sample Output: Bike

NOTE: In this example, we are only counting the blocks between ‘S’ and ‘D’ to compute the minimum time & dollar cost.

"""

# start 3:05PM
# end   4:22PM


from pprint import pprint
from typing import List, Tuple
import sys

def solve_path(grid: List[List[str]], transportation_modes: List[str], cost_matrix = List[int], time_matrix = List[int]) -> str:
    start_location = None
    end_location = None

    num_rows = len(grid)
    num_cols = len(grid[0])

    # get start and end
    for i, row in enumerate(grid):
        for j, val in enumerate(row):
            if val == 'S':
                start_location = (i, j)
            elif val == 'D':
                end_location = (i, j)
    
    if (not start_location) or (not end_location):
        raise ValueError(f"start and end locations must exist in grid")
    
    def get_min_path(transportation_mode) -> int:

        def get_valid_neighbors(index: Tuple[int, int]) -> List[Tuple[int, int]]:
            a = index[0] + 1, index[1]
            b = index[0], index[1] + 1
            c = index[0] - 1, index[1]
            d = index[0], index[1] - 1

            return [
                x for x 
                in [a,b,c,d] 
                if x[0] >= 0 and x[0] < num_rows \
                    and x[1] >= 0 and x[1] < num_cols \
                        and grid[x[0]][x[1]] in [str(transportation_mode), 'D' ]
                ]

        cost_grid: List[List[int]] = list()
        # index -> cost_from_start
        for i in range(num_rows):
            cost_grid.append(list())
            for j in range(num_cols):
                cost_grid[i].append(sys.maxsize)

        # (index, cost)
        # this needs to be a priority queue by lowest cost
        cell_queue: List[Tuple[Tuple[int, int], int]] = [(start_location, 0)]

        while len(cell_queue) > 0:
            current, cost = cell_queue.pop(0)

            if grid[current[0]][current[1]] == 'D':
                return cost

            if cost < cost_grid[current[0]][current[1]]:
                # we've found a cheaper way to get here
                cost_grid[current[0]][current[1]] = cost
                # this means we need to update neighbors
                next_cost = cost + 1
                valid_neighbors = [
                    (v, cost + 1) for v 
                    in get_valid_neighbors(current) 
                    if cost_grid[v[0]][v[1]] > next_cost
                    ]
                cell_queue = valid_neighbors + cell_queue

        # no solution
        return sys.maxsize

    dollar_cost_results: List = [None] * len(transportation_modes)
    time_cost_results: List   = [None] * len(transportation_modes)

    for transportation_mode in range(1, 5):
        len_path = get_min_path(transportation_mode)

        index = transportation_mode - 1
        time_cost = len_path * time_matrix[index]
        dollar_cost = len_path * cost_matrix[index]

        dollar_cost_results[index] = dollar_cost
        time_cost_results[index] = time_cost
    
    min_index = 0

    for i, time_cost in enumerate(time_cost_results):
        if time_cost < time_cost_results[min_index]:
            min_index = i
        elif time_cost == time_cost_results[min_index]:
            if dollar_cost_results[i] < dollar_cost_results[min_index]:
                min_index = i

    return transportation_modes[min_index]            

def test_1():
    test_grid = [
        ['3', '3', 'S', '2', 'X', 'X'],
        ['3', '1', '1', '2', 'X', '2'],
        ['3', '1', '1', '2', '2', '2'],
        ['3', '1', '1', '1', 'D', '3'],
        ['3', '3', '3', '3', '3', '4'],
        ['4', '4', '4', '4', '4', '4']
    ]

    # 1-based
    transportation_modes = ["Walk", "Bike", "Car", "Train"]
    cost_matrix = [0, 1, 3, 2]
    time_matrix = [3, 2, 1, 1]

    pprint(solve_path(test_grid, transportation_modes, cost_matrix, time_matrix))

    # find lowest time
    # if same, lowest cost

test_1()

