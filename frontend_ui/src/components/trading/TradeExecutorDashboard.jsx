import React, { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select";
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from "recharts";
import toast from "react-hot-toast";

const brokers = ["alpaca", "oanda", "ibr", "fxcm", "binance", "coinbase", "bybit"];

const dummyPerformanceData = [
  { name: "Binance", speed: 120, successRate: 95 },
  { name: "Coinbase", speed: 150, successRate: 92 },
  { name: "Bybit", speed: 100, successRate: 97 },
];

export default function TradeExecutorDashboard() {
  const [broker, setBroker] = useState("binance");
  const [symbol, setSymbol] = useState("");
  const [qty, setQty] = useState("");
  const [side, setSide] = useState("buy");
  const [leverage, setLeverage] = useState("");
  const [marginMode, setMarginMode] = useState("isolated");
  const [loading, setLoading] = useState(false);

  const handleExecute = async () => {
    if (!symbol || !qty || !leverage) {
      toast.error("Please fill in all required fields.");
      return;
    }

    const payload = {
      broker,
      symbol: symbol.toUpperCase().trim(),
      qty: parseFloat(qty),
      side,
      leverage: parseInt(leverage),
      margin_mode: marginMode
    };

    setLoading(true);

    try {
      const res = await fetch("/api/execute-trade", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Execution failed.");
      }

      const data = await res.json();
      toast.success(`✅ Trade executed on ${data.broker.toUpperCase()} (ID: ${data.orderId})`);
    } catch (err) {
      console.error(err);
      toast.error(`❌ Trade failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid gap-6 p-6">
      {/* Trade Execution Form */}
      <Card className="p-4">
        <h2 className="text-xl font-semibold mb-4">🚀 Broker Selector & Trade Execution</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Select value={broker} onValueChange={setBroker}>
            <SelectTrigger>
              <SelectValue placeholder="Select Broker" />
            </SelectTrigger>
            <SelectContent>
              {brokers.map((b) => (
                <SelectItem key={b} value={b}>{b.toUpperCase()}</SelectItem>
              ))}
            </SelectContent>
          </Select>

          <Input
            placeholder="Symbol (e.g. BTCUSDT)"
            value={symbol}
            onChange={e => setSymbol(e.target.value)}
          />

          <Input
            placeholder="Quantity"
            type="number"
            value={qty}
            onChange={e => setQty(e.target.value)}
          />

          <Select value={side} onValueChange={setSide}>
            <SelectTrigger>
              <SelectValue placeholder="Side" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="buy">Buy</SelectItem>
              <SelectItem value="sell">Sell</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
          <Input
            placeholder="Leverage (e.g. 5)"
            type="number"
            value={leverage}
            onChange={e => setLeverage(e.target.value)}
          />

          <Select value={marginMode} onValueChange={setMarginMode}>
            <SelectTrigger>
              <SelectValue placeholder="Margin Mode" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="isolated">Isolated</SelectItem>
              <SelectItem value="cross">Cross</SelectItem>
            </SelectContent>
          </Select>

          <Button
            onClick={handleExecute}
            className="col-span-2"
            disabled={loading}
          >
            {loading ? "Executing..." : "Execute Trade"}
          </Button>
        </div>
      </Card>

      {/* Broker Performance Chart */}
      <Card className="p-4">
        <h2 className="text-xl font-semibold mb-4">📊 Broker Comparison Dashboard</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart
            data={dummyPerformanceData}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <XAxis dataKey="name" />
            <YAxis yAxisId="left" orientation="left" stroke="#8884d8" />
            <YAxis yAxisId="right" orientation="right" stroke="#82ca9d" />
            <Tooltip />
            <Legend />
            <Bar
              yAxisId="left"
              dataKey="speed"
              fill="#8884d8"
              name="Execution Speed (ms)"
            />
            <Bar
              yAxisId="right"
              dataKey="successRate"
              fill="#82ca9d"
              name="Success Rate (%)"
            />
          </BarChart>
        </ResponsiveContainer>
      </Card>
    </div>
  );
}
