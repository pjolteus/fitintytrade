import React, { useEffect, useState } from 'react';
import { fetchPredictionHistory } from '../api/api';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorBanner from '../components/ErrorBanner';
import AssetChart from '../components/AssetChart';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import * as XLSX from 'xlsx';
import Plot from 'react-plotly.js';

function CurrencyDashboard() {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [filter, setFilter] = useState('');
  const [minConfidence, setMinConfidence] = useState(0);
  const [timeframe, setTimeframe] = useState('1m');

  useEffect(() => {
    const loadData = async () => {
      try {
        const all = await fetchPredictionHistory();
        const fxOnly = all.filter((p) => p.assetType === 'currency');
        setPredictions(fxOnly);
      } catch (err) {
        setError('Failed to load currency predictions.');
      } finally {
        setLoading(false);
      }
    };

    loadData();
    const interval = setInterval(loadData, 60000);
    return () => clearInterval(interval);
  }, []);

  // Filtered by user inputs
  const filtered = predictions
    .filter((p) =>
      (!filter || p.ticker.toLowerCase().includes(filter.toLowerCase())) &&
      p.confidence >= minConfidence
    )
    .filter((p) => {
      // Apply timeframe filter
      const now = new Date();
      const date = new Date(p.date);
      const diff = now - date;

      const limits = {
        '1h': 60 * 60 * 1000,
        '4h': 4 * 60 * 60 * 1000,
        '1d': 24 * 60 * 60 * 1000,
        '1m': 30 * 24 * 60 * 60 * 1000,
        '1y': 365 * 24 * 60 * 60 * 1000,
      };

      return diff <= limits[timeframe];
    });

  const exportPDF = () => {
    const doc = new jsPDF();
    doc.text('Currency Predictions Report', 14, 16);
    autoTable(doc, {
      startY: 20,
      head: [['Pair', 'Confidence', 'Prediction', 'Entry', 'Exit', 'Profit %', 'Date']],
      body: withPnL.map((p) => [
        p.ticker,
        `${(p.confidence * 100).toFixed(1)}%`,
        p.prediction === 1 ? 'Call' : 'Put',
        p.entryPrice ?? '—',
        p.exitPrice ?? '—',
        p.profit?.toFixed(2) + '%' ?? '—',
        new Date(p.date).toLocaleString(),
      ]),
    });
    doc.save('currency_predictions.pdf');
  };

  const exportCSV = () => {
    const worksheet = XLSX.utils.json_to_sheet(
      withPnL.map((p) => ({
        Pair: p.ticker,
        Confidence: `${(p.confidence * 100).toFixed(1)}%`,
        Prediction: p.prediction === 1 ? 'Call' : 'Put',
        Entry: p.entryPrice ?? '',
        Exit: p.exitPrice ?? '',
        Profit: p.profit?.toFixed(2) ?? '',
        Date: new Date(p.date).toLocaleString(),
      }))
    );
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Predictions');
    XLSX.writeFile(workbook, 'currency_predictions.xlsx');
  };

  // Profit calculations
  const withPnL = filtered
    .filter((p) => p.entryPrice && p.exitPrice)
    .map((p) => {
      const isCall = p.prediction === 1;
      const rawChange = ((p.exitPrice - p.entryPrice) / p.entryPrice) * 100;
      const profit = isCall ? rawChange : -rawChange;
      return { ...p, profit };
    });

  // Cumulative
  let cumulative = 0;
  const cumulativeData = withPnL.map((p) => {
    cumulative += p.profit;
    return { date: new Date(p.date).toLocaleDateString(), cumulative };
  });

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">💱 Currency Dashboard</h1>

      {/* Filters */}
      <div className="flex flex-wrap gap-4 items-center">
        <input
          type="text"
          placeholder="Filter by Pair"
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
          className="border p-2 rounded"
        >
          <option value="1h">1H</option>
          <option value="4h">4H</option>
          <option value="1d">1D</option>
          <option value="1m">1M</option>
          <option value="1y">1Y</option>
        </select>
        <button onClick={exportPDF} className="bg-purple-600 text-white px-3 py-1 rounded hover:bg-purple-700">
          Export PDF
        </button>
        <button onClick={exportCSV} className="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700">
          Export CSV
        </button>
      </div>

      {loading && <LoadingSpinner />}
      {error && <ErrorBanner message={error} />}

      {/* Confidence Chart */}
      <AssetChart data={filtered} title="Confidence Over Time (Currency)" />

      {/* Signal vs Actual */}
      {withPnL.length > 0 && (
        <div className="w-full h-[300px]">
          <h2 className="text-md font-semibold mb-2">Predicted vs Actual Market</h2>
          <Plot
            data={[
              {
                x: withPnL.map((p) => new Date(p.date).toLocaleDateString()),
                y: withPnL.map((p) => p.prediction === 1 ? p.entryPrice : p.entryPrice),
                type: 'scatter',
                mode: 'lines+markers',
                name: 'Predicted Direction (Entry)',
                line: { color: 'orange', dash: 'dot' },
              },
              {
                x: withPnL.map((p) => new Date(p.date).toLocaleDateString()),
                y: withPnL.map((p) => p.exitPrice),
                type: 'scatter',
                mode: 'lines+markers',
                name: 'Actual Exit Price',
                line: { color: 'green' },
              },
            ]}
            layout={{
              yaxis: { title: 'Price' },
              xaxis: { title: 'Date' },
              margin: { t: 30, b: 40, l: 40, r: 10 },
              plot_bgcolor: 'transparent',
              paper_bgcolor: 'transparent',
              font: { color: '#444' },
            }}
            config={{ responsive: true }}
          />
        </div>
      )}

      {/* Cumulative Profit Curve */}
      {withPnL.length > 0 && (
        <div className="w-full h-[300px]">
          <h2 className="text-md font-semibold mb-2">Cumulative Profit (%)</h2>
          <Plot
            data={[
              {
                x: cumulativeData.map((d) => d.date),
                y: cumulativeData.map((d) => d.cumulative),
                type: 'scatter',
                mode: 'lines+markers',
                line: { color: 'blue' },
              },
            ]}
            layout={{
              yaxis: { title: 'Cumulative Profit %' },
              xaxis: { title: 'Date' },
              margin: { t: 30, b: 40, l: 40, r: 10 },
              plot_bgcolor: 'transparent',
              paper_bgcolor: 'transparent',
              font: { color: '#444' },
            }}
            config={{ responsive: true }}
          />
        </div>
      )}

      {/* Entry vs Exit Price Chart */}
      {withPnL.length > 0 && (
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
              yaxis: { title: 'Price' },
              xaxis: { title: 'Date' },
              margin: { t: 30, b: 40, l: 40, r: 10 },
              plot_bgcolor: 'transparent',
              paper_bgcolor: 'transparent',
              font: { color: '#444' },
            }}
            config={{ responsive: true }}
          />
        </div>
      )}

      {/* Table */}
      <div className="overflow-x-auto border rounded shadow-sm">
        <table className="min-w-full text-sm text-left">
          <thead className="bg-gray-200 dark:bg-gray-700">
            <tr>
              <th className="px-4 py-2">Pair</th>
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
                <td className={`px-4 py-2 ${item.profit >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {item.profit.toFixed(2)}%
                </td>
                <td className="px-4 py-2">{new Date(item.date).toLocaleString()}</td>
              </tr>
            ))}
            {withPnL.length === 0 && (
              <tr>
                <td colSpan="7" className="px-4 py-6 text-center text-gray-500">
                  No currency predictions with entry/exit prices to calculate profit.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default CurrencyDashboard;
