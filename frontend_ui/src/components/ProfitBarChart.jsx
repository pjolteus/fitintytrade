// src/components/ProfitBarChart.jsx

import React from 'react';
import Plot from 'react-plotly.js';

function ProfitBarChart({ predictions = [], title = 'P/L Overview' }) {
  const bars = predictions
    .filter(p => p.entryPrice && p.exitPrice)
    .map(p => {
      const isCall = p.prediction === 1;
      const rawChange = ((p.exitPrice - p.entryPrice) / p.entryPrice) * 100;
      const profit = isCall ? rawChange : -rawChange;

      return {
        date: new Date(p.date).toLocaleDateString(),
        profit: parseFloat(profit.toFixed(2)),
        entry: p.entryPrice,
        exit: p.exitPrice,
        ticker: p.ticker,
      };
    });

  const colors = bars.map(b => (b.profit >= 0 ? 'green' : 'red'));

  return (
    <div className="w-full h-[300px]">
      <h2 className="text-md font-semibold mb-2">{title}</h2>
      <Plot
        data={[
          {
            x: bars.map(b => b.date),
            y: bars.map(b => b.profit),
            type: 'bar',
            marker: { color: colors },
            hovertext: bars.map(
              b => `${b.ticker}<br>Entry: ${b.entry}<br>Exit: ${b.exit}<br>PnL: ${b.profit}%`
            ),
          },
        ]}
        layout={{
          margin: { t: 30, b: 40, l: 40, r: 10 },
          yaxis: { title: 'Profit %', zeroline: true },
          xaxis: { title: 'Date' },
          bargap: 0.3,
          plot_bgcolor: 'transparent',
          paper_bgcolor: 'transparent',
          font: { color: '#444' },
        }}
        config={{ responsive: true }}
        style={{ width: '100%', height: '100%' }}
      />
    </div>
  );
}

export default ProfitBarChart;
