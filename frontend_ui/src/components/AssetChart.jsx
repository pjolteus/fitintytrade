import React from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';

function AssetChart({ data = [], title = 'Confidence Over Time' }) {
  const sorted = [...data]
    .filter((d) => d.date && d.confidence !== undefined)
    .sort((a, b) => new Date(a.date) - new Date(b.date));

  return (
    <div className="h-64 w-full">
      <h2 className="text-md font-semibold mb-2">{title}</h2>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={sorted}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" tickFormatter={(d) => new Date(d).toLocaleDateString()} />
          <YAxis domain={[0, 1]} tickFormatter={(v) => `${(v * 100).toFixed(0)}%`} />
          <Tooltip labelFormatter={(label) => new Date(label).toLocaleString()} />
          <Line type="monotone" dataKey="confidence" stroke="#8884d8" dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default AssetChart;
