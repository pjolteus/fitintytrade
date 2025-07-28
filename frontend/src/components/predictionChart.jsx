import React from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';

const PredictionChart = ({ history }) => {
  const chartData = history.map((item, index) => ({
    name: `${item.symbol}-${item.model_type}`,
    prob: Number(item.probability),
  })).reverse();

  return (
    <div className="mt-6 bg-white p-4 shadow rounded">
      <h2 className="text-lg font-semibold text-purple-700 mb-4">📈 Prediction Probability Chart</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis domain={[0, 1]} tickFormatter={(val) => `${val * 100}%`} />
          <Tooltip formatter={(val) => `${(val * 100).toFixed(2)}%`} />
          <Line type="monotone" dataKey="prob" stroke="#8B8000" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PredictionChart;
