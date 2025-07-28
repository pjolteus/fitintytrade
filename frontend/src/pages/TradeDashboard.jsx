// frontend_ui/src/pages/TradeDashboard.jsx

import React from "react";
import TradeExecutorDashboard from "../components/trading/TradeExecutorDashboard";

export default function TradeDashboard() {
  return (
    <div className="p-6 min-h-screen bg-gray-50">
      <h1 className="text-2xl font-bold mb-4 text-gray-800">Trade Executor Dashboard</h1>
      <TradeExecutorDashboard />
    </div>
  );
}
