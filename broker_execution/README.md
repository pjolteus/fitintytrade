# Broker Execution Module

This module handles trade execution, simulation, and strategy logic for FitintyTrade.

### Folders:
- `connectors/`: Unified interfaces to different brokers (Alpaca, FXCM, OANDA, Binance, etc.)
- `strategies/`: Risk management and trade selection logic
- `simulator/`: For backtesting trades
- `utils/`: Logging and helpers

Run `execute_trade.py` to execute live trades via the selected broker.
