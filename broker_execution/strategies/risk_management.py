
def apply_risk_management(entry_price, stop_loss_pct=0.02, take_profit_pct=0.05):
    stop_loss = entry_price * (1 - stop_loss_pct)
    take_profit = entry_price * (1 + take_profit_pct)
    return stop_loss, take_profit
