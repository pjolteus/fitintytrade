
def select_top_trades(predictions, top_n=5):
    sorted_preds = sorted(predictions, key=lambda x: x['confidence'], reverse=True)
    return sorted_preds[:top_n]
