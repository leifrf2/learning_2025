import os.path
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set
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
    original_quantity: int
    remaining_quantity: int
    is_cancelled: bool

    def __hash__(self):
        return super().__hash__()


@dataclass
class BuyOrder(Order):
    def __lt__(self, other: Any) -> bool:
        if type(other) is not BuyOrder:
            # don't want to compare SellOrders and BuyOrders
            raise ValueError(f"other order must be of type {BuyOrder} but is instead {type(other)}")
        else:
            if self.price > other.price:
                return True
            elif self.price < other.price:
                return False
            else:
                # equal on price
                # tie-break is whichever came first
                return other.timestamp > self.timestamp

    def __hash__(self):
        return super().__hash__()


@dataclass
class SellOrder(Order):
    def __lt__(self, other: Any) -> bool:
        if type(other) is not SellOrder:
            # don't want to compare SellOrders and BuyOrders
            raise ValueError(f"other order must be of type {SellOrder} but is instead {type(other)}")
        else:
            if self.price < other.price:
                return True
            elif self.price > other.price:
                return False
            else:
                # equal on price
                # tie-break is whichever came first
                return other.timestamp > self.timestamp

    def __hash__(self):
        return super().__hash__()
    

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
        self.buy_heap: List[BuyOrder] = list()
        self.sell_heap: List[SellOrder] = list()
        # it doesn't matter if they're buy or sell orders
        self.order_map: Dict[str, Dict[int, Set[Order]]] = dict()


    def _print_executed_order_segment(self,
                                      timestamp: int,
                                      buyer: str,
                                      seller: str,
                                      price: float,
                                      quantity: int) -> None:
        # handle the specific printing formatting that hackerrank produces
        formatted_price = int(price) if type(price) is float and price.is_integer() else price
        print(f"{timestamp},{buyer},{seller},{formatted_price},{quantity}")


    def _get_or_create_order_set(self, client_id: str, price: int) -> Set[Order]:
        if client_id not in self.order_map.keys():
            self.order_map[client_id] = dict()

        if price not in self.order_map[client_id]:
            self.order_map[client_id][price] = set()
        
        return self.order_map[client_id][price]


    def _add_order_to_map(self, order: Order) -> None:
        specific_order_map: Set[Order] = self._get_or_create_order_set(order.client_id, order.price)
        specific_order_map.add(order)


    def _remove_order_from_map(self, order: Order) -> None:
        specific_order_map: Set[Order] = self._get_or_create_order_set(order.client_id, order.price)
        specific_order_map.remove(order)
        # will leave an empty set if this is the last order
        # not a big deal, since this is on the scale of # of different clients & prices


    # generates a trade against any existing, unfilled sell orders
    # at the same or lower price. lowest price is preferred
    # at the price of the sell orders
    # if all or some of the buy cannot be matched against sell orders,
    # the unmatched quantity "rests" on the market for a later sell order to match against
    def execute_buy(self, buy_order: BuyOrder) -> None:
        while len(self.sell_heap) > 0 and buy_order.remaining_quantity > 0:
            sell_order = self.sell_heap[0]

            if sell_order.is_cancelled:
                # sell order is already not in map at this stage
                heapq.heappop(self.sell_heap)

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
                    self._remove_order_from_map(sell_order)
                    heapq.heappop(self.sell_heap)

                    self._print_executed_order_segment(
                        timestamp=buy_order.timestamp,
                        buyer=buy_order.client_id,
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
                        seller=sell_order.client_id,
                        price=sell_order.price,
                        quantity=buy_order.remaining_quantity
                    )

                    buy_order.remaining_quantity = 0


        if buy_order.remaining_quantity > 0:
            # we didn't completely exhaust this order
            heapq.heappush(self.buy_heap, buy_order)
            self._add_order_to_map(buy_order)


    # execute against any resting buy orders at the same or higher price
    # at the price of the buy orders
    # highest available price is preferred
    # same rest rules as execute_buy
    def execute_sell(self, sell_order: SellOrder) -> None:
        while len(self.buy_heap) > 0 and sell_order.remaining_quantity > 0:
            buy_order = self.buy_heap[0]

            if buy_order.is_cancelled:
                # buy order is already not in map at this stage
                heapq.heappop(self.buy_heap)

            elif buy_order.price < sell_order.price:
                # there are still sell orders resting
                # but they're not a fit
                break

            else:
                if buy_order.remaining_quantity <= sell_order.remaining_quantity:
                    # there isn't enough buy to exhaust this sell order
                    sell_order.remaining_quantity -= buy_order.remaining_quantity
                    heapq.heappop(self.buy_heap)
                    self._remove_order_from_map(buy_order)

                    self._print_executed_order_segment(
                        timestamp=sell_order.timestamp,
                        buyer=buy_order.client_id,
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
                        seller=sell_order.client_id,
                        price=buy_order.price,
                        quantity=sell_order.remaining_quantity
                    )

                    sell_order.remaining_quantity = 0

        if sell_order.remaining_quantity > 0:
            heapq.heappush(self.sell_heap, sell_order)
            self._add_order_to_map(sell_order)

    # when a cancel order arrives, all the CLIENT's resting
    # quantity at a given price is cancelled
    def execute_cancel(self, action: CancelAction):
        matching_orders = self._get_or_create_order_set(action.client_id, action.price)
        
        for order in matching_orders:
            order.is_cancelled = True
        
        matching_orders.clear()
    

    def execute_action(self, action: Action):
        if type(action) is BuyOrder:
            self.execute_buy(action)
        elif type(action) is SellOrder:
            self.execute_sell(action)
        elif type(action) is CancelAction:
            self.execute_cancel(action)
        else:
            raise ValueError(f"Unsupported action type: {type(action)}")


BUY = "B"
SELL = "S"
CANCEL = "C"
HEADER = "timestamp,client,action,price,quantity"


def resolve_action(
        timestamp: int,
        client_id :str,
        action: str, # B, S, or C
        price: float,
        quantity: int # zero for cancels
        ) -> Action:
    if action == BUY:
        return BuyOrder(
            timestamp=timestamp,
            client_id=client_id,
            price=price,
            original_quantity=quantity,
            remaining_quantity=quantity,
            is_cancelled=False
        )
    elif action == SELL:
        return SellOrder(
            timestamp=timestamp,
            client_id=client_id,
            price=price,
            original_quantity=quantity,
            remaining_quantity=quantity,
            is_cancelled=False
        )
    elif action == CANCEL:
        return CancelAction(
            timestamp=timestamp,
            client_id=client_id,
            price=price
        )
    else:
        raise ValueError(f"Unknown action type: {(action)}")


def main(filename: Optional[str] = None):
    if filename and os.path.isfile(filename):
        import fileinput
        stream_reader = fileinput.input(filename)
    else:
        stream_reader = sys.stdin

    exchange: Exchange = Exchange()

    for in_line in stream_reader:
        line = in_line.strip()
        if line == HEADER:
            continue

        action = None

        try:
            timestamp, client_id, action, price, quantity = line.split(',')
            action: Action = resolve_action(int(timestamp), client_id, action, float(price), int(quantity))
        except Exception as e:
            print(f"failed to parse line: {line}, exception:{e}")
        
        if action:
            exchange.execute_action(action)

if __name__ == "__main__":
    main("live_interviews/pdt/pdt_test_4.csv")

