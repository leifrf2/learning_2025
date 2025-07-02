from typing import List, Dict, Tuple
from pprint import pprint
import sys
# minimum coins
# given a set of coins [c1..cn] and a target sum of money m,
# what is the minimum number of coins that form up the sum m?

# example 1: [200, 100, 50, 20, 10, 5, 2, 1], 734 => 8
# example 2: [1,4,5], 13 => 3 (4,4,5)

coins_memo: Dict[int, int] = dict()

def min_coins(m: int, coins: List[int]) -> int:
    if m == 0:
        return 0
    elif len(coins) == 0:
        return sys.maxsize
    
    if m not in coins_memo.keys():
        # take coin
        take_coins = min_coins(m - coins[0], coins) + 1 if coins[0] <= m else sys.maxsize

        # don't take coin
        dont_take_coins = min_coins(m, coins[1:]) if len(coins) > 0 else sys.maxsize

        coins_memo[m] = min(take_coins, dont_take_coins)
    
    return coins_memo[m]

    # the minimum number of coins to produce m
    # is the minimum number of coins it takes to produce m-c for each c in coins

def min_coins_2(m: int, coins: List[int]) -> int:
    if m in coins_memo:
        return coins_memo[m]
    elif m == 0:
        return 0
    elif m < 0:
        return sys.maxsize
    
    answer = min(min_coins_2(m - c, coins) for c in coins) + 1
    coins_memo[m] = answer

    return answer

