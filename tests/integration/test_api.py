from fastapi.testclient import TestClient

from mcp_marketing_suite.api.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_generate_and_fetch_outputs(tmp_path):
    payload = {"product": "Acme", "audience": "CMO", "brand": "Direct", "goals": ["ROI"]}
    resp = client.post("/api/marketing/generate", json=payload)
    assert resp.status_code == 200
    request_id = resp.json()["request_id"]

    outputs = client.get(f"/api/marketing/outputs/{request_id}")
    assert outputs.status_code == 200
    assert "strategy.md" in outputs.json()["files"]
