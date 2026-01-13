import contextvars
import time
import uuid
from dataclasses import dataclass
from typing import Optional

from .logging_config import log

request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="-")


@dataclass
class TraceContext:
    request_id: str
    start_time: float

    @property
    def elapsed_ms(self) -> float:
        return (time.time() - self.start_time) * 1000


def new_request_id() -> str:
    rid = uuid.uuid4().hex
    request_id_var.set(rid)
    return rid


def get_request_id(default: Optional[str] = None) -> str:
    return request_id_var.get(default or "-")


def trace_operation(name: str, request_id: Optional[str] = None):
    rid = request_id or get_request_id()
    ctx = TraceContext(request_id=rid, start_time=time.time())

    class _Trace:
        def __enter__(self):
            log.info("start", extra={"request_id": ctx.request_id, "operation": name})
            return ctx

        def __exit__(self, exc_type, exc_val, exc_tb):
            status = "error" if exc_type else "ok"
            log.info(
                "end",
                extra={
                    "request_id": ctx.request_id,
                    "operation": name,
                    "status": status,
                    "elapsed_ms": round(ctx.elapsed_ms, 2),
                },
            )

    return _Trace()
