from fastapi.testclient import TestClient

from mcp_marketing_suite.api.main import app
from mcp_marketing_suite.config import get_settings

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_generate_and_fetch_outputs(tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUTS_DIR", str(tmp_path))
    get_settings.cache_clear()
    try:
        payload = {
            "product": "Acme",
            "audience": "CMO",
            "brand": "Direct",
            "goals": ["ROI"],
        }
        resp = client.post("/api/marketing/generate", json=payload)
        assert resp.status_code == 200
        response_json = resp.json()
        request_id = response_json["request_id"]
        assert response_json["output_dir"].startswith(str(tmp_path))

        outputs = client.get(f"/api/marketing/outputs/{request_id}")
        assert outputs.status_code == 200
        files = outputs.json()["files"]
        assert "strategy.md" in files
    finally:
        get_settings.cache_clear()
