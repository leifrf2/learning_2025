"""
Track balance, there are three funcs: 
create_grant (id, amount, timestamp, expiration time), 
subtract (amount, timestamp), 
get_balance (timestamp). 
Each grand has id, amount, timestamp, expiration_timestamp. 
Use timestamp to control get_balance. 
When withdrawing money, first withdraw from the oldest grand, but do not need to return. 
Only get_balance returns balance. It may subtract first and then create, so it will not get negative numbers.
"""

from datetime import datetime
from dataclasses import dataclass
from typing import List, Tuple
import heapq

@dataclass
class Grant:
    id: int
    amount: int
    remaining_amount: int
    timestamp: datetime
    expiration_timestamp: datetime
    is_expired: bool

    def __init__(self, id, amount, timestamp, expiration_timestamp):
        self.id = id
        self.amount = amount
        self.timestamp = timestamp
        self.expiration_timestamp=expiration_timestamp
        
        self.remaining_amount = self.amount
        self.is_expired = False

    @property
    def is_valid(self) -> bool:
        return (self.remaining_amount > 0) and (not self.is_expired)

class GrantManager:
    def __init__(self):
        self.expiration_heap: List[Tuple[int, Grant]] = list()
        self.grant_stack: List[Grant] = list()
        self.balance = 0

    def create_grant(self, id: int, amount: int, timestamp: datetime, expiration_time: datetime):
        new_grant: Grant = Grant(
            id=id,
            amount=amount,
            timestamp=timestamp,
            expiration_timestamp=expiration_time
        )

        heapq.heappush(self.expiration_heap, (new_grant.expiration_timestamp, new_grant))
        self.grant_stack.append(new_grant)
        self.balance += new_grant.amount

    def expire_grants(self, timestamp: datetime) -> None:
        while len(self.expiration_heap) > 0:
            top = self.expiration_heap[0][1]
            if top.expiration_timestamp < timestamp:
                # this is expired
                top.is_expired = True
                heapq.heappop(self.expiration_heap)
                self.balance -= top.remaining_amount
            else:
                # timestamp == expiration_timestamp is still valid
                # there are no more grants to expire
                break

    def subtract(self, amount: int, timestamp: datetime) -> None:
        # waht happens if withdrawing above the balance?
        # for now assume we just go to 0
        self.expire_grants(timestamp=timestamp)
        while amount > 0 and len(self.grant_stack) > 0:
            next_grant = self.grant_stack[0]

            if next_grant.is_valid:
                if next_grant.remaining_amount >= amount:
                    # can just deduct from this grant and be done
                    next_grant.remaining_amount -= amount
                    self.balance -= amount
                    amount = 0
                else:
                    # amount is greater than this grant
                    # consume the entire grant
                    amount -= next_grant.remaining_amount
                    self.balance -= next_grant.remaining_amount
                    next_grant.remaining_amount = 0
                    self.grant_stack.pop(0)
            else:
                self.grant_stack.pop(0)


    def get_balance(self, timestamp: datetime) -> int:
        self.expire_grants(timestamp)
        return self.balance