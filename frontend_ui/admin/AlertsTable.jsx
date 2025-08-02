import React, { useEffect, useState } from "react";
import { fetchAlerts } from "./api";

export default function AlertsTable({ token }) {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    fetchAlerts(token).then(setAlerts);
  }, [token]);

  return (
    <div>
      <h2 className="text-xl font-semibold mt-4">🔔 Alert Logs</h2>
      <table className="w-full text-sm mt-2">
        <thead>
          <tr className="border-b font-medium">
            <th>Type</th>
            <th>Symbol</th>
            <th>Message</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {alerts.map((a, i) => (
            <tr key={i} className="border-b">
              <td>{a.type}</td>
              <td>{a.symbol}</td>
              <td>{a.message}</td>
              <td>{new Date(a.timestamp).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

