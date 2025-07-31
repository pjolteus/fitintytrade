
def performance_by_asset_class(df):
    grouped = df.groupby('asset_type')['profit'].agg(['sum', 'mean', 'count'])
    grouped = grouped.rename(columns={'sum': 'Total Profit', 'mean': 'Avg Profit', 'count': 'Trades'})
    return grouped
