from pathlib import Path
from typing import Any, Dict

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from ..config import Settings, get_settings
from ..logging_config import log, setup_logging
from ..observability import get_request_id, new_request_id
from ..crew.orchestrator import get_orchestrator

app = FastAPI(title="MCP Marketing Suite", version="0.1.0")


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    rid = request.headers.get("x-request-id") or new_request_id()
    request.state.request_id = rid
    response = await call_next(request)
    response.headers["x-request-id"] = rid
    return response


def get_request_payload(request: Request) -> Dict[str, Any]:
    return {
        "product": request.state.payload.get("product"),
        "audience": request.state.payload.get("audience"),
        "brand": request.state.payload.get("brand"),
        "goals": request.state.payload.get("goals", []),
    }


@app.on_event("startup")
async def startup() -> None:
    settings = get_settings()
    setup_logging(settings.log_level)
    log.info("startup", extra={"env": settings.app_env})


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/api/marketing/generate")
async def generate(
    payload: Dict[str, Any], request: Request, settings: Settings = Depends(get_settings)
):
    rid = getattr(request.state, "request_id", new_request_id())
    request.state.payload = payload
    orchestrator = get_orchestrator()
    try:
        output_dir = Path("outputs") / rid
        result = orchestrator.run(payload, output_dir=output_dir)
        return JSONResponse({"request_id": rid, "output_dir": str(output_dir)})
    except Exception as exc:  # noqa: BLE001
        log.exception("generate_error", extra={"request_id": rid})
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/api/marketing/outputs/{request_id}")
async def get_outputs(request_id: str):
    output_dir = Path("outputs") / request_id
    if not output_dir.exists():
        raise HTTPException(status_code=404, detail="request_id not found")
    files = {p.name: p.read_text(encoding="utf-8") for p in output_dir.iterdir()}
    return {"request_id": request_id, "files": files}
