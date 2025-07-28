import React, { useState } from "react";
import AlertsTable from "./AlertsTable";
import PredictionsTable from "./PredictionsTable";

export default function AdminDashboard() {
  const [token, setToken] = useState("");

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold">FitintyTrade Admin</h1>
      <input
        type="password"
        placeholder="Enter Admin JWT Token"
        className="border p-2 w-full"
        value={token}
        onChange={(e) => setToken(e.target.value)}
      />
      {token && (
        <>
          <AlertsTable token={token} />
          <PredictionsTable token={token} />
        </>
      )}
    </div>
  );
}
