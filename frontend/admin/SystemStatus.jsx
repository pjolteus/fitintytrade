import React, { useEffect, useState } from "react";
import axios from "axios";

function SystemStatus() {
  const [healthStatus, setHealthStatus] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchStatus() {
      try {
        const health = await axios.get("/api/health");
        const metricRes = await axios.get("/api/metrics");
        setHealthStatus(health.data);
        setMetrics(metricRes.data);
        setLoading(false);
      } catch (error) {
        setHealthStatus({ status: "unreachable" });
        setLoading(false);
      }
    }

    fetchStatus();
    const interval = setInterval(fetchStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: "1rem" }}>
      <h2>System Status</h2>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <>
          <p>
            Backend API:{" "}
            <strong style={{ color: healthStatus?.status === "ok" ? "green" : "red" }}>
              {healthStatus?.status || "unknown"}
            </strong>
          </p>
          <p>
            Metrics:{" "}
            {metrics ? (
              <code style={{ whiteSpace: "pre-wrap", display: "block", background: "#eee", padding: "0.5rem" }}>
                {metrics.slice(0, 500)}...
              </code>
            ) : (
              <span style={{ color: "red" }}>Unavailable</span>
            )}
          </p>
        </>
      )}
    </div>
  );
}

export default SystemStatus;
