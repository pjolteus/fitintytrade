export async function fetchAlerts(token) {
  const res = await fetch("/api/admin/alerts", {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.json();
}

export async function fetchPredictions(token) {
  const res = await fetch("/api/admin/predictions", {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.json();
}

