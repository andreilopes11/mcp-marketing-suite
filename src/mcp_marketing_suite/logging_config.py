import logging
import sys
from typing import Any, Dict

try:  # pragma: no cover - optional dependency
    from pythonjsonlogger.json import JsonFormatter
except ModuleNotFoundError:  # pragma: no cover
    JsonFormatter = None


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:  # noqa: A003
        if not hasattr(record, "request_id"):
            record.request_id = "-"
        return True


def setup_logging(level: str = "INFO") -> None:
    handler = logging.StreamHandler(sys.stdout)
    if JsonFormatter:
        formatter = JsonFormatter("%(levelname)s %(name)s %(message)s %(request_id)s")
    else:
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s")
    handler.setFormatter(formatter)
    handler.addFilter(RequestIdFilter())

    root = logging.getLogger()
    root.setLevel(level.upper())
    root.handlers.clear()
    root.addHandler(handler)


log: logging.Logger = logging.getLogger("mcp_marketing_suite")


def log_extra(request_id: str | None = None, **kwargs: Any) -> Dict[str, Any]:
    extra = {"request_id": request_id or "-"}
    extra.update(kwargs)
    return extra
