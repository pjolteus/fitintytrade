import React, { useEffect, useState } from 'react';
import { getPrediction, startTraining } from '../api/api';
import Top10List from "../components/Top10List";
import PredictionChart from "../components/PredictionChart";
import ModelComparisonChart from "../components/ModelComparisonChart";

const MODEL_TYPES = ["lstm", "gru", "transformer", "tcn"];

const OverviewDashboard = () => {
  const [symbol, setSymbol] = useState('');
  const [modelType, setModelType] = useState('lstm');
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState(() => {
    const saved = localStorage.getItem('prediction_history');
    return saved ? JSON.parse(saved) : [];
  });

  const handlePredict = async () => {
    if (!symbol.trim()) {
      alert("Please enter a valid symbol.");
      return;
    }

    setLoading(true);
    try {
      const res = await getPrediction(symbol, modelType);
      if (res.status === "success") {
        setPrediction(res);
        const newHistory = [res, ...history].slice(0, 10);
        setHistory(newHistory);
        localStorage.setItem('prediction_history', JSON.stringify(newHistory));
      } else {
        alert("Prediction failed: " + res.message);
      }
    } catch (err) {
      console.error(err);
      alert("Error occurred during prediction.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Top10List />
      <div className="min-h-screen bg-purple-50 p-6">
        <h1 className="text-2xl font-bold text-purple-700 mb-4">📊 FitintyTrade Overview</h1>

        <div className="flex flex-col sm:flex-row items-center gap-4 mb-6">
          <input
            className="p-2 border rounded w-full sm:w-1/3"
            type="text"
            placeholder="Enter stock or currency symbol (e.g., AAPL)"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value.toUpperCase())}
          />
          <select
            className="p-2 border rounded"
            value={modelType}
            onChange={(e) => setModelType(e.target.value)}
          >
            {MODEL_TYPES.map(type => (
              <option key={type} value={type}>{type.toUpperCase()}</option>
            ))}
          </select>
          <button
            className="bg-yellow-700 text-white px-4 py-2 rounded"
            onClick={handlePredict}
          >
            {loading ? "Predicting..." : "Get Prediction"}
          </button>
          <button
            className="bg-purple-700 text-white px-4 py-2 rounded"
            onClick={() => startTraining()}
          >
            Start Training
          </button>
        </div>

        {loading && <p className="text-sm text-gray-600">Fetching prediction...</p>}

        {prediction && (
          <div className="bg-white p-4 rounded shadow mb-6">
            <h2 className="text-lg font-semibold text-purple-800">🔍 Latest Prediction</h2>
            <p><strong>Symbol:</strong> {prediction.symbol}</p>
            <p><strong>Model:</strong> {prediction.model_type.toUpperCase()}</p>
            <p><strong>Prediction:</strong> {prediction.prediction ? "UP" : "DOWN"}</p>
            <p><strong>Confidence:</strong> {(prediction.probability * 100).toFixed(2)}%</p>
          </div>
        )}

        {history.length > 0 && (
          <div className="bg-white p-4 rounded shadow mb-6">
            <h3 className="text-lg font-semibold text-purple-700 mb-2">📜 Prediction History</h3>
            <ul className="list-disc ml-6 text-sm">
              {history.map((item, idx) => (
                <li key={idx}>
                  {item.symbol} ({item.model_type.toUpperCase()}): {item.prediction ? "↑" : "↓"} @ {(item.probability * 100).toFixed(2)}%
                </li>
              ))}
            </ul>
          </div>
        )}

        {history.length > 1 && (
          <>
            <PredictionChart history={history} />
            <ModelComparisonChart history={history} />
          </>
        )}
      </div>
    </>
  );
};

export default OverviewDashboard;
