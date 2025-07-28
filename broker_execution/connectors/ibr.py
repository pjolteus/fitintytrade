
import os
import logging
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_fixed

from ib_insync import IB, MarketOrder, StopOrder, LimitOrder, TrailingStopOrder, Forex, Stock

load_dotenv()

IB_HOST = os.getenv("IBR_HOST", "127.0.0.1")
IB_PORT = int(os.getenv("IBR_PORT", 7497))  # 7496 = live; 7497 = paper
IB_CLIENT_ID = int(os.getenv("IBR_CLIENT_ID", 1))

# Global IB connection
ib = IB()
ib.connect(IB_HOST, IB_PORT, clientId=IB_CLIENT_ID)

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def place_order(symbol: str, qty: int, side: str, stop_loss=None, take_profit=None, trailing_stop=None, is_forex=False):
    """
    Place a market or bracket order on IBKR using ib-insync.
    """
    contract = Forex(symbol) if is_forex else Stock(symbol, 'SMART', 'USD')
    ib.qualifyContracts(contract)

    action = "BUY" if side == "buy" else "SELL"
    orders = []

    # Primary market order
    primary_order = MarketOrder(action, qty)

    # Add bracket orders
    if stop_loss or take_profit or trailing_stop:
        if trailing_stop:
            stop_order = TrailingStopOrder(action="SELL" if side == "buy" else "BUY", totalQuantity=qty, trailingPercent=trailing_stop)
            orders.append(stop_order)
        elif stop_loss:
            stop_order = StopOrder(action="SELL" if side == "buy" else "BUY", totalQuantity=qty, stopPrice=stop_loss)
            orders.append(stop_order)

        if take_profit:
            limit_order = LimitOrder(action="SELL" if side == "buy" else "BUY", totalQuantity=qty, lmtPrice=take_profit)
            orders.append(limit_order)

    # Submit the primary order
    trade = ib.placeOrder(contract, primary_order)

    # Submit bracket legs
    for leg in orders:
        ib.placeOrder(contract, leg)

    ib.sleep(1)
    return {"orderId": trade.order.orderId, "status": trade.orderStatus.status}


def get_order_status(order_id: int):
    orders = ib.reqAllOpenOrders()
    for o in orders:
        if o.order.orderId == order_id:
            return {
                "orderId": o.order.orderId,
                "status": o.orderStatus.status,
                "filled": o.orderStatus.filled,
                "remaining": o.orderStatus.remaining
            }
    raise Exception(f"Order ID {order_id} not found")


def cancel_order(order_id: int):
    orders = ib.reqAllOpenOrders()
    for o in orders:
        if o.order.orderId == order_id:
            ib.cancelOrder(o.order)
            return {"status": "cancelled", "order_id": order_id}
    raise Exception(f"Cancel failed: Order ID {order_id} not found")

def get_all_positions():
    return [
        {
            "symbol": pos.contract.symbol,
            "qty": abs(pos.position)
        } for pos in ib.positions()
    ]


def get_position(symbol: str, is_forex=False):
    positions = ib.positions()
    for pos in positions:
        if symbol in pos.contract.symbol:
            return {
                "symbol": pos.contract.symbol,
                "qty": pos.position,
                "avg_price": pos.avgCost
            }
    return None
