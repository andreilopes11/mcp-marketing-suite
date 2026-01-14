from pathlib import Path
from typing import Any, Dict

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from ..config import Settings, get_settings
from ..logging_config import log, setup_logging
from ..observability import new_request_id
from ..crew.orchestrator import get_orchestrator
from .schemas import GenerateRequest

app = FastAPI(title="MCP Marketing Suite", version="0.1.0")


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    rid = request.headers.get("x-request-id") or new_request_id()
    request.state.request_id = rid
    response = await call_next(request)
    response.headers["x-request-id"] = rid
    return response


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
    request_body: GenerateRequest, request: Request, settings: Settings = Depends(get_settings)
):
    rid = getattr(request.state, "request_id", new_request_id())
    orchestrator = get_orchestrator(settings=settings)
    try:
        output_dir = Path(settings.outputs_dir) / rid
        result = orchestrator.run(request_body, output_dir=output_dir)
        response_payload = {"request_id": rid, "output_dir": str(output_dir)}
        if result.get("bundle"):
            response_payload["bundle"] = result["bundle"]
        return JSONResponse(response_payload)
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
