import requests

def check_health():
    res = requests.get("https://your-api-url.onrender.com/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

def check_metrics():
    res = requests.get("https://your-api-url.onrender.com/metrics")
    assert "python_info" in res.text

if __name__ == "__main__":
    try:
        check_health()
        check_metrics()
        print("✅ Deployment check passed.")
    except Exception as e:
        print("❌ Deployment check failed:", str(e))
