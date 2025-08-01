// 📂 File: frontend/src/pages/BrokerInfo.jsx
import React, { useEffect, useState } from "react";
import axios from "axios";

function BrokerInfo() {
  const [brokers, setBrokers] = useState({});

  useEffect(() => {
    axios.get("/api/broker-info").then(res => setBrokers(res.data));
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">📊 Broker Metadata</h2>
      <table className="min-w-full border">
        <thead>
          <tr>
            <th>Broker</th>
            <th>Leverage</th>
            <th>Margin</th>
            <th>Commission (%)</th>
            <th>Assets</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(brokers).map(([name, data]) => (
            <tr key={name}>
              <td>{name}</td>
              <td>{data.max_leverage}x</td>
              <td>{(data.margin_required * 100).toFixed(1)}%</td>
              <td>{data.commission}%</td>
              <td>{data.asset_types.join(", ")}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default BrokerInfo;
