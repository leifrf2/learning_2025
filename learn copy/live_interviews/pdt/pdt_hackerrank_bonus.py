# Enter your code here. Read input from STDIN. Print output to STDOUT

"""
(The original problem did not include symbols)

Theory:
    Incoming sell order A
        Get buy orders for client, symbol of A
            If any buy orders are greater than A
            Strike all the matching orders

Changes:
1. Add a dictionary to Exchange with mapping: Dict[Client_id, Dict[Symbol, Tuple[Heap[BuyOrder], Heap[SellOrder]]]]
2. When an order is completed from Resting by the exchange, mark it is_completed=True
3. When a new order is being processed...
    1. Look up the correlating heap in the client and symbol map
    2. iteratively pop is_cancelled=True and is_completed=True elements from the heap
    3. if there is a remaining record and it violates the condition
        1. get all orders from the client in the parent dictionary and flag them is_cancelled=True
    4. otherwise, process the order as normal
        1. if the order is put in resting, add it to the appropriate heap in the client_symbol map

This adds another pointer for every Resting element.
The memory complexity does not increase from this, but it is of practical significance.

The individual heaps in the client_symbol map would be expected to be small in the general case.
A hot shard could still make them large, such as a symbol whose earnings event is coming up.
The cost is logK for the K elements in the heap, if all of them need to be popped off.

"""

from dataclasses import dataclass
from typing import Any, Dict, List, Set, Tuple
import heapq
import sys

@dataclass
class Action:
    timestamp: int
    client_id: str
    price: float

    def __hash__(self):
        # timesetamp is unique and immutable, per the problem description
        return self.timestamp


@dataclass
class Order(Action):
    symbol: str
    original_quantity: int
    remaining_quantity: int
    is_cancelled: bool
    is_completed: bool

    def __hash__(self):
        return super().__hash__()

    @property
    def is_viable(self):
        return not (self.is_cancelled or self.is_completed)


@dataclass
class BuyOrder(Order):
    def __lt__(self, other: Any) -> bool:
        if isinstance(other, BuyOrder):
            if self.price > other.price:
                return True
            elif self.price < other.price:
                return False
            else:
                # equal on price
                # tie-break is whichever came first
                return other.timestamp > self.timestamp
        else:
         # don't want to compare SellOrders and BuyOrders
            raise ValueError(f"other order must be of type {BuyOrder} but is instead {type(other)}")

    def __hash__(self):
        return super().__hash__()


@dataclass
class BuyOrderMinHeap(BuyOrder):
    def __init__(self,
                 buy_order: BuyOrder):
        self.buy_order = buy_order
    
    def __lt__(self, other):
        if isinstance(other, BuyOrderMinHeap):
            return not self.buy_order.__lt__(other.buy_order)
        raise ValueError(f"other is of invalid type {type(other)}")


@dataclass
class SellOrder(Order):
    def __lt__(self, other: Any) -> bool:
        if isinstance(other, SellOrder):
            if self.price < other.price:
                return True
            elif self.price > other.price:
                return False
            else:
                # equal on price
                # tie-break is whichever came first
                return other.timestamp > self.timestamp
        else:
            # don't want to compare SellOrders and BuyOrders
            raise ValueError(f"other order must be of type {SellOrder} but is instead {type(other)}")

    def __hash__(self):
        return super().__hash__()
    

@dataclass
class SellOrderMaxHeap(SellOrder):
    def __init__(self,
                 sell_order: SellOrder):
        self.sell_order = sell_order
    
    def __lt__(self, other):
        if isinstance(other, SellOrderMaxHeap):
            return not self.sell_order.__lt__(other.sell_order)
        else:
            raise ValueError(f"other is of invalid type {type(other)}")


@dataclass
class CancelAction(Action):
    pass


# if two or more clients have resting orders at the same price
# and a matching order is submitted, the orders are
# eligible for matching in the order they were submitted
# clients can trade against themself

# may be a very large number of orders, price levels, and clients
# stream input and output, do not buffer
class Exchange:
    def __init__(self):
        # symbol -> buy_heap
        self.buy_heaps: Dict[str, List[BuyOrder]] = dict()
        # symbol -> sell+_heap
        self.sell_heaps: Dict[str, List[SellOrder]] = dict()
        # it doesn't matter if they're buy or sell orders
        self.cancel_order_map: Dict[str, Dict[int, Set[Order]]] = dict()        
        # client -> symbol -> orders
        self.client_symbol_map: Dict[str, Dict[str, Tuple[List[BuyOrderMinHeap], List[SellOrderMaxHeap]]]] = dict()


    def _print_executed_order_segment(self,
                                      timestamp: int,
                                      buyer: str,
                                      seller: str,
                                      symbol: str,
                                      price: float,
                                      quantity: int) -> None:
        # handle the specific printing formatting that hackerrank produces
        formatted_price = int(price) if type(price) is float and price.is_integer() else price
        print(f"{timestamp},{buyer},{seller},{symbol},{formatted_price},{quantity}")


    def _get_or_create_order_cancel_set(self, client_id: str, price: int) -> Set[Order]:
        if client_id not in self.cancel_order_map.keys():
            self.cancel_order_map[client_id] = dict()

        if price not in self.cancel_order_map[client_id]:
            self.cancel_order_map[client_id][price] = set()
        
        return self.cancel_order_map[client_id][price]


    def _get_or_create_client_symbol_orders(self, client_id: str, symbol: str) -> Tuple[List[BuyOrderMinHeap], List[SellOrderMaxHeap]]:
        if client_id not in self.client_symbol_map.keys():
            self.client_symbol_map[client_id] = dict()

        if symbol not in self.client_symbol_map[client_id].keys():
            self.client_symbol_map[client_id][symbol] = (list(), list())
        
        return self.client_symbol_map[client_id][symbol]
        

    def _get_or_create_symbol_heap_buy(self, symbol: str) -> List[BuyOrder]:
        if symbol not in self.buy_heaps.keys():
            self.buy_heaps[symbol] = list()
        
        return self.buy_heaps[symbol]


    def _get_or_create_symbol_heap_sell(self, symbol: str) -> List[SellOrder]:
        if symbol not in self.sell_heaps.keys():
            self.sell_heaps[symbol] = list()
        
        return self.sell_heaps[symbol]


    def _remove_order_from_cancel_map(self, order: Order) -> None:
        specific_order_map: Set[Order] = self._get_or_create_order_cancel_set(order.client_id, order.price)
        specific_order_map.remove(order)
        # will leave an empty set if this is the last order
        # not a big deal, since this is on the scale of # of different clients & prices


    def _add_order_to_resting(self, order: Order) -> None:
        # add to nested order map for cancels
        # buy vs sell doesn't matter here
        specific_order_map: Set[Order] = self._get_or_create_order_cancel_set(order.client_id, order.price)
        specific_order_map.add(order)

        # add to client_symbol order map for violations
        client_specific_buy_heap, client_specific_sell_heap = self._get_or_create_client_symbol_orders(order.client_id, order.symbol)

        if type(order) is BuyOrder:
            heapq.heappush(client_specific_buy_heap, BuyOrderMinHeap(order))
            symbol_heap = self._get_or_create_symbol_heap_buy(order.symbol)
            heapq.heappush(symbol_heap, order)
        elif type(order) is SellOrder:
            heapq.heappush(client_specific_sell_heap, SellOrderMaxHeap(order))
            symbol_heap = self._get_or_create_symbol_heap_sell(order.symbol)
            heapq.heappush(symbol_heap, order)
        else:
            raise ValueError(f"Unsupported order type {type(order)}")


    def _check_order_is_valid(self, order: Order) -> bool:
        buy_stack, sell_stack = self._get_or_create_client_symbol_orders(order.client_id, order.symbol)

        if type(order) is SellOrder:
            if len(buy_stack) > 0:
                while len(buy_stack) > 0 and not buy_stack[0].buy_order.is_viable:
                    heapq.heappop(buy_stack)
                    # get to the lowest viable order

                if len(buy_stack) > 0:
                    lowest_buy_price = buy_stack[0].buy_order.price

                    # order price must be greater than
                    # the lowest buy price here for it to be valid
                    return order.price > lowest_buy_price
                else:
                    # there are no more orders, so no violation can occur
                    return False
            else:
                return True
            
        elif type(order) is BuyOrder:
            if len(sell_stack) > 0:
                while len(sell_stack) > 0 and not sell_stack[0].sell_order.is_viable:
                    heapq.heappop(sell_stack)
                
                if len(sell_stack) > 0:
                    highest_sell_price = sell_stack[0].sell_order.price

                    # order price must be less than
                    # the highest buy price here for it to be valid
                    return order.price < highest_sell_price
                else:
                    # no more orders, no more violation possible
                    return False
            else:
                return True

        else:
            raise ValueError(f"Unsupported order type: {type(order)}")


    def _cancel_client_orders(self, client_id: str) -> None:
        # cancel all the orders of this client
        
        for _, (buy_order_wrappers, sell_order_wrappers) in self.client_symbol_map.get(client_id, dict()).items():
            for buy_order_wrapper in buy_order_wrappers:
                buy_order_wrapper.buy_order.is_cancelled = True

            for sell_order_wrapper in sell_order_wrappers:
                sell_order_wrapper.sell_order.is_cancelled = True


    # generates a trade against any existing, unfilled sell orders
    # at the same or lower price. lowest price is preferred
    # at the price of the sell orders
    # if all or some of the buy cannot be matched against sell orders,
    # the unmatched quantity "rests" on the market for a later sell order to match against
    def execute_buy(self, buy_order: BuyOrder) -> None:
        sell_heap = self._get_or_create_symbol_heap_sell(buy_order.symbol)

        while len(sell_heap) > 0 and buy_order.remaining_quantity > 0:
            sell_order = sell_heap[0]

            if sell_order.is_cancelled:
                # sell order is already not in map at this stage
                heapq.heappop(sell_heap)

            elif sell_order.price > buy_order.price:
                # there are still sell orders resting
                # but they're too expensive for this buy order
                break

            else:
                # implied: sell_order.price <= buy_order.price:
                # order will buy it
                if sell_order.remaining_quantity <= buy_order.remaining_quantity:
                    # there isn't necessarily enough to exhaust this order
                    buy_order.remaining_quantity -= sell_order.remaining_quantity
                    self._remove_order_from_cancel_map(sell_order)
                    heapq.heappop(sell_heap)
                    sell_order.is_completed = True

                    self._print_executed_order_segment(
                        timestamp=buy_order.timestamp,
                        buyer=buy_order.client_id,
                        symbol=buy_order.symbol,
                        seller=sell_order.client_id,
                        price=sell_order.price,
                        quantity=sell_order.remaining_quantity
                    )

                else:
                    # there is greater than or enough in this sell order
                    # so we we will not be adding the buy to the heap
                    sell_order.remaining_quantity -= buy_order.remaining_quantity

                    self._print_executed_order_segment(
                        timestamp=buy_order.timestamp,
                        buyer=buy_order.client_id,
                        symbol=buy_order.symbol,
                        seller=sell_order.client_id,
                        price=sell_order.price,
                        quantity=buy_order.remaining_quantity
                    )

                    buy_order.remaining_quantity = 0


        if buy_order.remaining_quantity > 0:
            self._add_order_to_resting(buy_order)


    # execute against any resting buy orders at the same or higher price
    # at the price of the buy orders
    # highest available price is preferred
    # same rest rules as execute_buy
    def execute_sell(self, sell_order: SellOrder) -> None:
        buy_heap = self._get_or_create_symbol_heap_buy(sell_order.symbol)

        while len(buy_heap) > 0 and sell_order.remaining_quantity > 0:
            buy_order = buy_heap[0]

            if buy_order.is_cancelled:
                # buy order is already not in map at this stage
                heapq.heappop(buy_heap)

            elif buy_order.price < sell_order.price:
                # there are still sell orders resting
                # but they're not a fit
                break

            else:
                if buy_order.remaining_quantity <= sell_order.remaining_quantity:
                    # there isn't enough buy to exhaust this sell order
                    sell_order.remaining_quantity -= buy_order.remaining_quantity
                    heapq.heappop(buy_heap)
                    self._remove_order_from_cancel_map(buy_order)
                    buy_order.is_completed = True

                    self._print_executed_order_segment(
                        timestamp=sell_order.timestamp,
                        buyer=buy_order.client_id,
                        symbol=sell_order.symbol,
                        seller=sell_order.client_id,
                        price=buy_order.price,
                        quantity=buy_order.remaining_quantity
                    )
                    
                else:
                    # there is more than enough quantity remaining in this buy
                    buy_order.remaining_quantity -= sell_order.remaining_quantity

                    self._print_executed_order_segment(
                        timestamp=sell_order.timestamp,
                        buyer=buy_order.client_id,
                        symbol=sell_order.symbol,
                        seller=sell_order.client_id,
                        price=buy_order.price,
                        quantity=sell_order.remaining_quantity
                    )

                    sell_order.remaining_quantity = 0

        if sell_order.remaining_quantity > 0:
            self._add_order_to_resting(sell_order)


    # when a cancel order arrives, all the CLIENT's resting
    # quantity at a given price is cancelled
    def execute_cancel(self, action: CancelAction):
        matching_orders = self._get_or_create_order_cancel_set(action.client_id, action.price)
        
        for order in matching_orders:
            order.is_cancelled = True
        
        matching_orders.clear()
    

    def execute_action(self, action: Action):
        if type(action) is BuyOrder:
            if self._check_order_is_valid(action):
                self.execute_buy(action)
            else:
                self._cancel_client_orders(action.client_id)

        elif type(action) is SellOrder:
            if self._check_order_is_valid(action):
                self.execute_sell(action)
            else:
                self._cancel_client_orders(action.client_id)

        elif type(action) is CancelAction:
            self.execute_cancel(action)

        else:
            raise ValueError(f"Unsupported action type: {type(action)}")


BUY = "B"
SELL = "S"
CANCEL = "C"


def resolve_action(
        timestamp: int,
        client_id :str,
        action: str, # B, S, or C
        symbol: str,
        price: float,
        quantity: int # zero for cancels
        ) -> Action:
    if action == BUY:
        return BuyOrder(
            timestamp=timestamp,
            client_id=client_id,
            symbol=symbol,
            price=price,
            original_quantity=quantity,
            remaining_quantity=quantity,
            is_cancelled=False,
            is_completed=False
        )
    elif action == SELL:
        return SellOrder(
            timestamp=timestamp,
            client_id=client_id,
            symbol=symbol,
            price=price,
            original_quantity=quantity,
            remaining_quantity=quantity,
            is_cancelled=False,
            is_completed=False            
        )
    elif action == CANCEL:
        return CancelAction(
            timestamp=timestamp,
            client_id=client_id,
            price=price
        )
    else:
        raise ValueError(f"Unknown action type: {(action)}")


def main():
    exchange: Exchange = Exchange()

    for in_line in sys.stdin:
        line = in_line.strip()

        action = None

        try:
            timestamp, client_id, action, symbol, price, quantity = line.split(',')
            action: Action = resolve_action(int(timestamp), client_id, action, symbol, float(price), int(quantity))
        except Exception as e:
            print(f"failed to parse line: {line}, exception:{e}")
        
        if action:
            exchange.execute_action(action)

if __name__ == "__main__":
    main()

