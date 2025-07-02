from typing import List
from pdt_hackerrank import Exchange, Action, BuyOrder, SellOrder, CancelAction


def create_buyorder(timestamp: int, client: str, price: float, quantity: int) -> BuyOrder:
    return BuyOrder(
            timestamp=timestamp,
            client_id=client,
            price=price,
            original_quantity=quantity,
            remaining_quantity=quantity,
            is_cancelled=False
        )


def create_sellorder(timestamp: int, client: str, price: float, quantity: int) -> SellOrder:
    return SellOrder(
            timestamp=timestamp,
            client_id=client,
            price=price,
            original_quantity=quantity,
            remaining_quantity=quantity,
            is_cancelled=False
        )


class Timestamp:
    def __init__(self):
        self.timestamp: int = 1

    @property
    def ts(self):
        ts = self.timestamp
        self.timestamp += 1
        return ts


def test_1000_buys(capsys):
    exchange = Exchange()
    client: str = 'A'
    price: float = 10.0
    quantity: int = 5

    for timestamp in range(1, 1001):
        action = BuyOrder(
            timestamp=timestamp,
            client_id=client,
            price=price,
            original_quantity=quantity,
            remaining_quantity=quantity,
            is_cancelled=False
        )

        exchange.execute_action(action)


def test_1000_sells(capsys):
    exchange = Exchange()
    client: str = 'A'
    price: float = 10.0
    quantity: int = 5

    for timestamp in range(1, 1001):
        action = SellOrder(
            timestamp=timestamp,
            client_id=client,
            price=price,
            original_quantity=quantity,
            remaining_quantity=quantity,
            is_cancelled=False
        )

        exchange.execute_action(action)


def test_1000_cancels(capsys):
    exchange = Exchange()
    client: str = 'A'
    price: float = 10.0

    for timestamp in range(1, 1001):
        action = CancelAction(
            timestamp=timestamp,
            client_id=client,
            price=price
        )

        exchange.execute_action(action)
    

def test_N_cancels_buy():
    # add a whole bunch of actions
    # and cancel all of them
    # and check that the internal state is empty
    buy_price = 10
    buy_quant = 50
    buy_client = 'a'

    # buy price will take this
    sell_price = 1
    sell_quant = 50
    sell_client = 'b'

    buy_count = 10
    sell_count = 10

    timestamp: int = 1

    exchange = Exchange()

    for _ in range(0, buy_count):
        order = create_buyorder(timestamp, buy_client, buy_price, buy_quant)
        exchange.execute_action(order)
        timestamp += 1
    
    for _ in range(0, buy_count):
        order = CancelAction(timestamp, buy_client, buy_price)
        exchange.execute_action(order)
        timestamp += 1
    
    for _ in range(0, sell_count):
        order = create_sellorder(timestamp, sell_client, sell_price, sell_quant)
        exchange.execute_action(order)
        timestamp += 1
    

def test_buy_sells(capsys):
    # add a whole bunch of actions
    # and cancel all of them
    # and check that the internal state is empty
    buy_price = 10
    buy_quant = 50
    buy_client = 'a'

    # buy price will take this
    sell_price = 1
    sell_quant = 50
    sell_client = 'b'

    buy_count = 10
    sell_count = 10

    timestamp: int = 1

    exchange = Exchange()

    for _ in range(0, buy_count):
        order = create_buyorder(timestamp, buy_client, buy_price, buy_quant)
        exchange.execute_action(order)
        timestamp += 1
    
    for _ in range(0, sell_count):
        order = create_sellorder(timestamp, sell_client, sell_price, sell_quant)
        exchange.execute_action(order)
        captured_out = capsys.readouterr().out
        assert captured_out == f'{timestamp},a,b,10,50\n'
        timestamp += 1


def test_segmented_buys(capsys):
    
    ts = Timestamp()
    exchange = Exchange()

    actions: List[Action] = [
        create_sellorder(ts.ts, 'a', 3, 5), # 15 total shares
        create_sellorder(ts.ts, 'a', 3, 5),
        create_sellorder(ts.ts, 'a', 3, 5),
        create_buyorder(ts.ts, 'a', 3, 15)
    ]

    for action in actions:
        exchange.execute_action(action)

    assert capsys.readouterr().out == '4,a,a,3,5\n4,a,a,3,5\n4,a,a,3,5\n'


def test_segmented_buys_with_leftover(capsys):
    
    ts = Timestamp()
    exchange = Exchange()

    actions: List[Action] = [
        create_sellorder(ts.ts, 'a', 3, 5), # 15 total shares
        create_sellorder(ts.ts, 'a', 3, 5),
        create_sellorder(ts.ts, 'a', 3, 5),
        create_buyorder(ts.ts, 'a', 3, 20)
    ]

    for action in actions:
        exchange.execute_action(action)

    assert capsys.readouterr().out == '4,a,a,3,5\n4,a,a,3,5\n4,a,a,3,5\n'
    assert len(exchange.buy_heap) == 1
    assert exchange.buy_heap[0].remaining_quantity == 5


def test_segmented_sells(capsys):
    
    ts = Timestamp()
    exchange = Exchange()

    actions: List[Action] = [
        create_buyorder(ts.ts, 'a', 3, 5), # 15 total shares
        create_buyorder(ts.ts, 'a', 3, 5),
        create_buyorder(ts.ts, 'a', 3, 5),
        create_sellorder(ts.ts, 'b', 3, 15)
    ]

    for action in actions:
        exchange.execute_action(action)

    assert capsys.readouterr().out == '4,a,b,3,5\n4,a,b,3,5\n4,a,b,3,5\n'


def test_segmented_sells_with_leftover(capsys):
    
    ts = Timestamp()
    exchange = Exchange()

    actions: List[Action] = [
        create_buyorder(ts.ts, 'b', 3, 5), # 15 total shares
        create_buyorder(ts.ts, 'b', 3, 5),
        create_buyorder(ts.ts, 'b', 3, 5),
        create_sellorder(ts.ts, 'a', 3, 20)
    ]

    for action in actions:
        exchange.execute_action(action)

    assert capsys.readouterr().out == '4,b,a,3,5\n4,b,a,3,5\n4,b,a,3,5\n'
    assert len(exchange.sell_heap) == 1
    assert exchange.sell_heap[0].remaining_quantity == 5

