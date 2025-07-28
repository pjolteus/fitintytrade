import torch
import numpy as np
import os
from evaluation.metrics import compute_classification_metrics
from evaluation.visuals import plot_confusion_and_roc, plot_confusion_and_roc_plotly
from evaluation.logger import save_metrics_to_json, append_log_entry
from evaluation.profit_curve import simulate_trades, plot_profit_curve, plot_profit_curve_plotly


def evaluate_model(
    model,
    dataloader,
    prices=None,
    model_name="model",
    threshold=0.5,
    device="cpu",
    save_dir="evaluation_outputs",
    use_plotly=False,
):
    model.eval()
    predictions, targets, predicted_probs = [], [], []

    with torch.no_grad():
        for X_batch, y_batch in dataloader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            output = model(X_batch)
            prob = torch.sigmoid(output).squeeze()
            pred = (prob > threshold).float()
            predicted_probs.extend(prob.cpu().numpy())
            predictions.extend(pred.cpu().numpy())
            targets.extend(y_batch.cpu().numpy())

    # Compute metrics
    metrics = compute_classification_metrics(targets, predictions, predicted_probs)

    # Print to console
    for k, v in metrics.items():
        print(f"{k}: {v:.4f}")

    # Create directory for saving outputs
    os.makedirs(save_dir, exist_ok=True)

    # Visual diagnostics
    if use_plotly:
        plot_confusion_and_roc_plotly(
            targets,
            predicted_probs,
            model_name=model_name,
            save_dir=save_dir
        )
    else:
        plot_confusion_and_roc(
            targets,
            predicted_probs,
            model_name=model_name,
            save_dir=save_dir
        )

    # Profit curve
    if prices is not None:
        df, profit, benchmark = simulate_trades(prices, np.array(predicted_probs), threshold=threshold)
        profit_path = os.path.join(save_dir, f"{model_name}_profit_curve.png")
        if use_plotly:
            plot_profit_curve_plotly(df, save_path=profit_path.replace(".png", ".html"))
        else:
            plot_profit_curve(df, save_path=profit_path)
        metrics["Profit ($)"] = profit
        metrics["Benchmark ($)"] = benchmark

    # Save metrics & logs
    save_metrics_to_json(metrics, model_name=model_name, output_dir=save_dir)
    append_log_entry(
        f"Evaluated {model_name} with F1={metrics['F1 Score']:.4f} and Profit=${metrics.get('Profit ($)', 0):.2f}",
        log_file=os.path.join(save_dir, "evaluation_log.txt")
    )

    return metrics
