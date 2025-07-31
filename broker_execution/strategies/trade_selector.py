from typing import List, Dict


def select_top_trades_with_allocation(
    predictions: List[Dict],
    total_capital: float = 10000.0,
    top_n: int = 6,
    min_confidence: float = 0.6,
    exclude_bankrupt: bool = True,
    diversify_by: str = "asset_type",  # options: 'asset_type', 'sector', 'pair'
    allocation_method: str = "score_weighted",  # or 'equal'
) -> List[Dict]:
    """
    Select top trades with intelligent filtering, diversification, and capital allocation.

    Args:
        predictions: List of prediction dicts with keys like confidence, asset_type, expected_profit, etc.
        total_capital: Total capital available for allocation.
        top_n: Maximum number of trades to return.
        min_confidence: Minimum confidence required to consider a trade.
        exclude_bankrupt: Whether to exclude tickers flagged as high bankruptcy risk.
        diversify_by: Key to diversify on (e.g., asset_type, sector, pair).
        allocation_method: 'score_weighted' or 'equal'.

    Returns:
        List of top trade dicts with 'allocated_capital' and 'score' fields added.
    """

    # Step 1: Filter by confidence and bankruptcy
    filtered = [
        p for p in predictions
        if p.get("confidence", 0) >= min_confidence and
           (not exclude_bankrupt or not p.get("is_bankrupt", False))
    ]

    if not filtered:
        return []

    # Step 2: Compute score = confidence × expected_profit (or fallback to confidence only)
    for trade in filtered:
        confidence = trade.get("confidence", 0)
        expected_profit = trade.get("expected_profit", 1)
        trade["score"] = confidence * expected_profit

    # Step 3: Sort by score descending
    sorted_trades = sorted(filtered, key=lambda x: x["score"], reverse=True)

    # Step 4: Enforce diversification (e.g., no duplicate asset_types)
    seen_keys = set()
    diversified = []
    for trade in sorted_trades:
        key = trade.get(diversify_by, "unknown")
        if key not in seen_keys:
            diversified.append(trade)
            seen_keys.add(key)
        if len(diversified) >= top_n:
            break

    # Step 5: Allocate capital
    if allocation_method == "equal":
        equal_amount = round(total_capital / len(diversified), 2)
        for trade in diversified:
            trade["allocated_capital"] = equal_amount
    else:  # score_weighted
        total_score = sum(t["score"] for t in diversified) or 1  # prevent division by zero
        for trade in diversified:
            weight = trade["score"] / total_score
            trade["allocated_capital"] = round(weight * total_capital, 2)

    return diversified
