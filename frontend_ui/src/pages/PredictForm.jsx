import React, { useState } from 'react';

function PredictForm() {
  const [ticker, setTicker] = useState('');
  const [interval, setInterval] = useState('1h');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    try {
      const res = await fetch('http://localhost:8000/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify({ ticker, interval }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Prediction failed');
      setResult(data);
    } catch (error) {
      setResult({ error: error.message });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded shadow max-w-lg mx-auto">
      <h2 className="text-2xl font-semibold text-purple-800 mb-4">Real-Time Prediction</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          placeholder="Enter Ticker (e.g., AAPL)"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
          required
          className="w-full border p-2 rounded"
        />
        <select
          value={interval}
          onChange={(e) => setInterval(e.target.value)}
          className="w-full border p-2 rounded"
        >
          <option value="1m">1m</option>
          <option value="15m">15m</option>
          <option value="1h">1h</option>
          <option value="1d">1d</option>
        </select>
        <button type="submit" className="w-full bg-purple-700 text-white py-2 rounded">
          Predict
        </button>
      </form>

      {loading && <p className="mt-4 text-gray-500">Loading prediction...</p>}

      {result && (
        <div className="mt-6 p-4 border rounded bg-gray-50">
          {result.error ? (
            <p className="text-red-600">{result.error}</p>
          ) : (
            <>
              <p>
                <strong>{result.ticker}</strong>: {result.prediction === 1 ? 'Bullish (Call)' : 'Bearish (Put)'}
              </p>
              <p className="text-sm text-gray-500">
                Confidence: {(result.confidence * 100).toFixed(2)}% | Model: {result.model_name}
              </p>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default PredictForm;
