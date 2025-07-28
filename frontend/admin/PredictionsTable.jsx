import React, { useEffect, useState } from "react";
import { fetchPredictions } from "./api";

export default function PredictionsTable({ token }) {
  const [preds, setPreds] = useState([]);

  useEffect(() => {
    fetchPredictions(token).then(setPreds);
  }, [token]);

  return (
    <div>
      <h2 className="text-xl font-semibold mt-6">📈 Predictions</h2>
      <table className="w-full text-sm mt-2">
        <thead>
          <tr className="border-b font-medium">
            <th>Ticker</th>
            <th>Confidence</th>
            <th>Feedback</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {preds.map((p, i) => (
            <tr key={i} className="border-b">
              <td>{p.ticker}</td>
              <td>{(p.confidence * 100).toFixed(2)}%</td>
              <td>{p.feedback}</td>
              <td>{new Date(p.created_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

