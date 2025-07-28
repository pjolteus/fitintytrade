from abc import ABC, abstractmethod
from typing import Optional, Dict

class BaseBrokerConnector(ABC):
    @abstractmethod
    def place_order(
        self,
        symbol: str,
        qty: int,
        side: str,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
        trailing_stop: Optional[float] = None,
        trailing_take_profit: Optional[float] = None
    ) -> Dict:
        pass

    @abstractmethod
    def cancel_order(self, order_id: str) -> Dict:
        pass

    @abstractmethod
    def get_order_status(self, order_id: str) -> Dict:
        pass

    @abstractmethod
    def get_position(self, symbol: str) -> Optional[Dict]:
        pass
