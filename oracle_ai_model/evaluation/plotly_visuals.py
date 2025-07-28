# evaluation/plotly_visuals.py
import plotly.graph_objs as go

def plot_profit_comparison(results):
    """
    Plot cumulative strategy returns and benchmark for multiple models.
    Input:
        results: list of dicts with keys:
            - name
            - profit
            - df (must contain 'cumulative_strategy' and 'cumulative_returns')
    """
    traces = []
    for res in results:
        df = res['df']
        traces.append(go.Scatter(
            x=df.index,
            y=df['cumulative_strategy'],
            mode='lines',
            name=f"{res['name']} (Profit=${res['profit']:.2f})"
        ))

    # Add market benchmark
    if results:
        traces.append(go.Scatter(
            x=results[0]['df'].index,
            y=results[0]['df']['cumulative_returns'],
            mode='lines',
            name="Market Benchmark",
            line=dict(dash='dot')
        ))

    layout = go.Layout(
        title="Model Profit Comparison",
        xaxis=dict(title="Time"),
        yaxis=dict(title="Cumulative Return"),
        hovermode='closest'
    )
    fig = go.Figure(data=traces, layout=layout)
    fig.show()
