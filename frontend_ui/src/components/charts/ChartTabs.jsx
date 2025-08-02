import React, { useState } from 'react';
import {
  LineChart, Line, XAxis, YAxis, Tooltip, Legend, CartesianGrid,
  PieChart, Pie, Cell,
  BarChart, Bar
} from 'recharts';

const COLORS = ['#8b5cf6', '#f43f5e', '#10b981', '#f59e0b', '#3b82f6'];

function ChartTabs({ data, comparisonMode = false, toggleEnabled = false, onSelectRow = () => {}, selectedIds = [] }) {
  const [activeTab, setActiveTab] = useState('line');
  const [useAverage, setUseAverage] = useState(false);

  const pieData = [
    {
      name: 'Call',
      value: data.filter(d => d.prediction === 1).length,
    },
    {
      name: 'Put',
      value: data.filter(d => d.prediction === 0).length,
    },
  ];

  const confidenceByTicker = Object.entries(
    data.reduce((acc, curr) => {
      acc[curr.ticker] = acc[curr.ticker] || [];
      acc[curr.ticker].push(curr.confidence * 100);
      return acc;
    }, {})
  ).map(([ticker, confidences]) => ({
    ticker,
    avgConfidence:
      confidences.reduce((sum, c) => sum + c, 0) / confidences.length,
  }));

  const handleSelect = (id) => {
    onSelectRow(id);
  };

  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow mt-6">
      <div className="flex gap-4 mb-4 flex-wrap items-center">
        {['line', 'pie', 'bar'].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-1 rounded ${
              activeTab === tab
                ? 'bg-purple-700 text-white'
                : 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-white'
            }`}
          >
            {tab === 'line' && 'Confidence Over Time'}
            {tab === 'pie' && 'Call vs Put'}
            {tab === 'bar' && 'Avg Confidence by Ticker'}
          </button>
        ))}

        {toggleEnabled && activeTab === 'line' && (
          <button
            onClick={() => setUseAverage(!useAverage)}
            className="ml-auto px-3 py-1 text-sm rounded bg-indigo-500 text-white"
          >
            Toggle: {useAverage ? 'Average' : 'Raw'}
          </button>
        )}
      </div>

      {activeTab === 'line' && (
        <LineChart width={700} height={300} data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="timestamp"
            tickFormatter={(v) => new Date(v).toLocaleDateString()}
          />
          <YAxis />
          <Tooltip />
          <Legend />
          {comparisonMode ? (
            [...new Set(data.map(d => d.ticker))].map((ticker, idx) => (
              <Line
                key={ticker}
                type="monotone"
                dataKey={(d) => d.ticker === ticker ? d.confidence * 100 : null}
                name={`Confidence: ${ticker}`}
                stroke={COLORS[idx % COLORS.length]}
                dot={false}
                data={data.filter(d => d.ticker === ticker)}
              />
            ))
          ) : (
            <Line
              type="monotone"
              dataKey={(d) => d.confidence * 100}
              name="Confidence %"
              stroke="#8b5cf6"
              dot={false}
            />
          )}
        </LineChart>
      )}

      {activeTab === 'pie' && (
        <PieChart width={400} height={300}>
          <Pie
            data={pieData}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={100}
            fill="#8884d8"
            label
          >
            {pieData.map((_, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index]} />
            ))}
          </Pie>
          <Legend />
        </PieChart>
      )}

      {activeTab === 'bar' && (
        <BarChart width={700} height={300} data={confidenceByTicker}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="ticker" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="avgConfidence" fill="#8b5cf6" />
        </BarChart>
      )}

      {onSelectRow && (
        <div className="mt-6">
          <h3 className="text-md font-semibold text-gray-700 dark:text-gray-200 mb-2">Select Predictions:</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
            {data.map((d) => (
              <label
                key={d.id}
                className="flex items-center space-x-2 bg-gray-100 dark:bg-gray-700 p-2 rounded"
              >
                <input
                  type="checkbox"
                  checked={selectedIds.includes(d.id)}
                  onChange={() => handleSelect(d.id)}
                />
                <span className="text-sm text-gray-800 dark:text-white">
                  {d.ticker} — {d.confidence.toFixed(2)} ({d.prediction === 1 ? 'Call' : 'Put'})
                </span>
              </label>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default ChartTabs;
