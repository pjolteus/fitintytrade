// Stock Dashboard
import React, { useEffect, useState } from 'react';
import { fetchPredictionHistory } from '../api/api';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorBanner from '../components/ErrorBanner';
import AssetChart from '../components/AssetChart';
import Plot from 'react-plotly.js';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import * as XLSX from 'xlsx';

function StockDashboard() {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [filter, setFilter] = useState('');
  const [minConfidence, setMinConfidence] = useState(0);
  const [timeframe, setTimeframe] = useState('1m'); // default timeframe

  useEffect(() => {
    const loadData = async () => {
      try {
        const all = await fetchPredictionHistory();
        const relevant = all.filter((p) => p.assetType === 'stock');
        setPredictions(relevant);
      } catch {
        setError('Failed to load predictions.');
      } finally {
        setLoading(false);
      }
    };

    loadData();
    const interval = setInterval(loadData, 60000);
    return () => clearInterval(interval);
  }, []);

  const filtered = predictions.filter(
    (p) =>
      (!filter || p.ticker.toLowerCase().includes(filter.toLowerCase())) &&
      p.confidence >= minConfidence
  );

  const timeframeFiltered = filtered.filter((p) => {
    const now = new Date();
    const predictionDate = new Date(p.date);
    const delta = now - predictionDate;
    switch (timeframe) {
      case '1h': return delta <= 3600000;
      case '4h': return delta <= 4 * 3600000;
      case '1d': return delta <= 86400000;
      case '1m': return delta <= 30 * 86400000;
      case '1y': return delta <= 365 * 86400000;
      default: return true;
    }
  });

  const withPnL = timeframeFiltered
    .filter((p) => p.entryPrice && p.exitPrice)
    .map((p) => {
      const isCall = p.prediction === 1;
      const rawChange = ((p.exitPrice - p.entryPrice) / p.entryPrice) * 100;
      const profit = isCall ? rawChange : -rawChange;
      return { ...p, profit };
    });

  let cumulative = 0;
  const cumulativeData = withPnL.map((p) => {
    cumulative += p.profit;
    return { date: new Date(p.date).toLocaleDateString(), cumulative };
  });

  const exportPDF = () => {
    const doc = new jsPDF();
    doc.text('Stock Predictions Report', 14, 16);
    autoTable(doc, {
      startY: 20,
      head: [['Ticker', 'Confidence', 'Prediction', 'Entry', 'Exit', 'Profit %', 'Date']],
      body: withPnL.map((p) => [
        p.ticker,
        `${(p.confidence * 100).toFixed(1)}%`,
        p.prediction === 1 ? 'Call' : 'Put',
        p.entryPrice ?? '—',
        p.exitPrice ?? '—',
        (p.profit != null ? p.profit.toFixed(2) + '%' : '—'),
        new Date(p.date).toLocaleString(),
      ]),
    });
    doc.save('stock_predictions.pdf');
  };

  const exportCSV = () => {
    const worksheet = XLSX.utils.json_to_sheet(
      withPnL.map((p) => ({
        Ticker: p.ticker,
        Confidence: `${(p.confidence * 100).toFixed(1)}%`,
        Prediction: p.prediction === 1 ? 'Call' : 'Put',
        Entry: p.entryPrice ?? '',
        Exit: p.exitPrice ?? '',
        Profit: p.profit?.toFixed(2) ?? '',
        Date: new Date(p.date).toLocaleString(),
      }))
    );
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Stock Predictions');
    XLSX.writeFile(workbook, 'stock_predictions.xlsx');
  };

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">📈 Stock Dashboard</h1>

      {/* Filters */}
      <div className="flex flex-wrap gap-4">
        <input
          type="text"
          placeholder="Filter by Ticker"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="border p-2 rounded w-60"
        />
        <input
          type="number"
          placeholder="Min Confidence"
          value={minConfidence}
          min="0"
          max="1"
          step="0.01"
          onChange={(e) => setMinConfidence(parseFloat(e.target.value))}
          className="border p-2 rounded w-40"
        />
        <select
          value={timeframe}
          onChange={(e) => setTimeframe(e.target.value)}
          className="border p-2 rounded w-40"
        >
          <option value="1h">Last 1 hour</option>
          <option value="4h">Last 4 hours</option>
          <option value="1d">Last 1 day</option>
          <option value="1m">Last 1 month</option>
          <option value="1y">Last 1 year</option>
        </select>
        <button
          onClick={exportPDF}
          className="bg-purple-600 text-white px-3 py-1 rounded hover:bg-purple-700"
        >
          Export PDF
        </button>
        <button
          onClick={exportCSV}
          className="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700"
        >
          Export CSV
        </button>
      </div>

      {loading && <LoadingSpinner />}
      {error && <ErrorBanner message={error} />}

      <AssetChart data={timeframeFiltered} title="Stock Confidence Over Time" />

      {withPnL.length > 0 && (
        <>
          <div className="w-full h-[300px]">
            <h2 className="text-md font-semibold mb-2">Cumulative Profit (%)</h2>
            <Plot
              data={[{
                x: cumulativeData.map((d) => d.date),
                y: cumulativeData.map((d) => d.cumulative),
                type: 'scatter',
                mode: 'lines+markers',
                line: { color: 'blue' },
              }]}
              layout={{
                margin: { t: 30, b: 40, l: 40, r: 10 },
                yaxis: { title: 'Cumulative Profit %' },
                xaxis: { title: 'Date' },
                plot_bgcolor: 'transparent',
                paper_bgcolor: 'transparent',
                font: { color: '#444' },
              }}
              config={{ responsive: true }}
            />
          </div>

          <div className="w-full h-[300px]">
            <h2 className="text-md font-semibold mb-2">Entry vs Exit Prices</h2>
            <Plot
              data={[
                {
                  x: withPnL.map((p) => new Date(p.date).toLocaleDateString()),
                  y: withPnL.map((p) => p.entryPrice),
                  type: 'scatter',
                  mode: 'lines+markers',
                  name: 'Entry Price',
                  line: { color: 'orange' },
                },
                {
                  x: withPnL.map((p) => new Date(p.date).toLocaleDateString()),
                  y: withPnL.map((p) => p.exitPrice),
                  type: 'scatter',
                  mode: 'lines+markers',
                  name: 'Exit Price',
                  line: { color: 'green' },
                },
              ]}
              layout={{
                margin: { t: 30, b: 40, l: 40, r: 10 },
                yaxis: { title: 'Price' },
                xaxis: { title: 'Date' },
                plot_bgcolor: 'transparent',
                paper_bgcolor: 'transparent',
                font: { color: '#444' },
              }}
              config={{ responsive: true }}
            />
          </div>
        </>
      )}

      <div className="overflow-x-auto border rounded shadow-sm">
        <table className="min-w-full text-sm text-left">
          <thead className="bg-gray-200 dark:bg-gray-700">
            <tr>
              <th className="px-4 py-2">Ticker</th>
              <th className="px-4 py-2">Confidence</th>
              <th className="px-4 py-2">Prediction</th>
              <th className="px-4 py-2">Entry Price</th>
              <th className="px-4 py-2">Exit Price</th>
              <th className="px-4 py-2">Profit %</th>
              <th className="px-4 py-2">Date</th>
            </tr>
          </thead>
          <tbody>
            {withPnL.map((item, idx) => (
              <tr key={idx} className="border-t">
                <td className="px-4 py-2">{item.ticker}</td>
                <td className="px-4 py-2">{(item.confidence * 100).toFixed(1)}%</td>
                <td className="px-4 py-2">{item.prediction === 1 ? '📈 Call' : '📉 Put'}</td>
                <td className="px-4 py-2">{item.entryPrice}</td>
                <td className="px-4 py-2">{item.exitPrice}</td>
                <td className={`px-4 py-2 ${item.profit >= 0 ? 'text-green-600' : 'text-red-600'}`}>{item.profit.toFixed(2)}%</td>
                <td className="px-4 py-2">{new Date(item.date).toLocaleString()}</td>
              </tr>
            ))}
            {withPnL.length === 0 && (
              <tr>
                <td colSpan="7" className="px-4 py-6 text-center text-gray-500">
                  No stock predictions with entry/exit prices to calculate profit.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default StockDashboard;
