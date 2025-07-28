# File: comparison_tools.py
import torch
import numpy as np
from evaluation.profit_curve import simulate_trades


def get_model_predictions(model, dataloader, device="cpu"):
    model.eval()
    probs = []
    with torch.no_grad():
        for X_batch, _ in dataloader:
            X_batch = X_batch.to(device)
            output = model(X_batch)
            prob = torch.sigmoid(output).squeeze()
            probs.extend(prob.cpu().numpy())
    return np.array(probs)


def compare_models_on_profit(models_info, df_prices, threshold=0.5):
    results = []
    for info in models_info:
        name, model, dataloader = info["name"], info["model"], info["dataloader"]
        probs = get_model_predictions(model, dataloader, device=next(model.parameters()).device)
        df_result, profit, benchmark = simulate_trades(df_prices.copy(), probs, threshold=threshold)
        results.append({"name": name, "df": df_result, "profit": profit, "benchmark": benchmark})
    return results
