// src/components/Top10List.jsx
import React, { useEffect, useState } from "react";
import { useApi } from "../hooks/useApi";

const Top10List = () => {
  const { fetchTop10Signals } = useApi();
  const [calls, setCalls] = useState([]);
  const [puts, setPuts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadSignals = async () => {
      try {
        const res = await fetchTop10Signals();
        setCalls(res.data.calls || []);
        setPuts(res.data.puts || []);
      } catch (err) {
        console.error("Failed to fetch Top10 signals:", err);
        setError("Unable to load trading signals. Please try again later.");
      } finally {
        setLoading(false);
      }
    };

    loadSignals();
  }, [fetchTop10Signals]);

  return (
    <div className="p-4 bg-white dark:bg-gray-900 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold text-purple-700 dark:text-purple-300 mb-4">
        📌 Top 10 Trading Signals
      </h2>

      {loading && <p className="text-gray-500 dark:text-gray-400">Loading...</p>}
      {error && <p className="text-red-600 dark:text-red-400">{error}</p>}

      {!loading && !error && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="text-lg font-bold text-green-600 dark:text-green-400 mb-2">Calls</h3>
            <ul className="list-disc ml-5 space-y-1">
              {calls.length > 0 ? (
                calls.map((item, idx) => (
                  <li key={idx}>
                    {item.symbol} – {(item.confidence * 100).toFixed(1)}%
                  </li>
                ))
              ) : (
                <li className="text-sm text-gray-500 dark:text-gray-400">No call signals.</li>
              )}
            </ul>
          </div>

          <div>
            <h3 className="text-lg font-bold text-red-600 dark:text-red-400 mb-2">Puts</h3>
            <ul className="list-disc ml-5 space-y-1">
              {puts.length > 0 ? (
                puts.map((item, idx) => (
                  <li key={idx}>
                    {item.symbol} – {(item.confidence * 100).toFixed(1)}%
                  </li>
                ))
              ) : (
                <li className="text-sm text-gray-500 dark:text-gray-400">No put signals.</li>
              )}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default Top10List;
