import React, { useEffect, useState } from "react";
import axios from "axios";

function LogViewer({ type = "backend" }) {
  const [logContent, setLogContent] = useState("");
  const [error, setError] = useState(false);

  const logPath = `/logs/${type}.log`;

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const res = await axios.get(logPath);
        setLogContent(res.data);
        setError(false);
      } catch (err) {
        setError(true);
        setLogContent(`Failed to load ${logPath}`);
      }
    };

    fetchLogs();
    const interval = setInterval(fetchLogs, 5000);
    return () => clearInterval(interval);
  }, [type]);

  return (
    <div style={{ padding: "1rem", background: "#111", color: "#0f0", fontFamily: "monospace", height: "400px", overflowY: "scroll" }}>
      <h3>{type}.log</h3>
      {error ? <p style={{ color: "red" }}>{logContent}</p> : <pre>{logContent}</pre>}
    </div>
  );
}

export default LogViewer;
