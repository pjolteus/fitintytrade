// frontend_ui/src/pages/TradeDashboard.jsx

import React from "react";
import TradeExecutorDashboard from "../components/trading/TradeExecutorDashboard";

export default function TradeDashboard() {
  return (
    <section className="min-h-screen bg-gray-50 dark:bg-gray-900 p-6">
      <header className="mb-6">
        <h1 className="text-3xl font-bold text-gray-800 dark:text-white">
          Trade Executor Dashboard
        </h1>
        <p className="text-sm text-gray-500 dark:text-gray-300 mt-1">
          Monitor signals, select brokers, and trigger trades
        </p>
      </header>

      <TradeExecutorDashboard />
    </section>
  );
}
