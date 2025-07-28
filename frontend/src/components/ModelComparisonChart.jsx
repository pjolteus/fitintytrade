import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

const ModelComparisonChart = ({ history }) => {
  // Group and average prediction confidence per model type
  const grouped = history.reduce((acc, item) => {
    const model = item.model_type.toUpperCase();
    acc[model] = acc[model] || { total: 0, count: 0 };
    acc[model].total += item.probability * 100;
    acc[model].count += 1;
    return acc;
  }, {});

  const chartData = Object.entries(grouped).map(([model, { total, count }]) => ({
    model,
    avg_confidence: (total / count).toFixed(2),
  }));

  return (
    <div className="bg-white p-4 rounded shadow mt-6">
      <h3 className="text-lg font-semibold text-purple-700 mb-4">📊 Model Accuracy Comparison</h3>
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="model" />
          <YAxis domain={[0, 100]} unit="%" />
          <Tooltip />
          <Bar dataKey="avg_confidence" fill="#8B8000" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ModelComparisonChart;
