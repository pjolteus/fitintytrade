// Top 10 trading signals list component 
// src/components/Top10List.jsx

import React, { useEffect, useState } from "react";
import { fetchTop10Signals } from "../services/api";

const Top10List = () => {
  const [calls, setCalls] = useState([]);
  const [puts, setPuts] = useState([]);

  useEffect(() => {
    fetchTop10Signals()
      .then((res) => {
        setCalls(res.data.calls);
        setPuts(res.data.puts);
      })
      .catch((err) => console.error("Failed to fetch Top10:", err));
  }, []);

  return (
    <div className="p-4 bg-white rounded shadow">
      <h2 className="text-xl font-semibold text-purple-700">📌 Top 10 Trading Signals</h2>
      <div className="grid grid-cols-2 gap-4 mt-4">
        <div>
          <h3 className="text-lg font-bold text-green-600">Calls</h3>
          <ul className="list-disc ml-4">
            {calls.map((item, idx) => (
              <li key={idx}>{item.symbol} – {(item.confidence * 100).toFixed(1)}%</li>
            ))}
          </ul>
        </div>
        <div>
          <h3 className="text-lg font-bold text-red-600">Puts</h3>
          <ul className="list-disc ml-4">
            {puts.map((item, idx) => (
              <li key={idx}>{item.symbol} – {(item.confidence * 100).toFixed(1)}%</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Top10List;
