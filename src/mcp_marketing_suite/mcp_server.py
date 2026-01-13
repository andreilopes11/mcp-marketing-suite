from typing import Any, Dict, List

from .logging_config import log, log_extra
from .observability import get_request_id
from .resources import load_mock_contexts
from .tools import (
    GenerateAds,
    GenerateCRMSequences,
    GenerateSEOPlan,
    GenerateStrategy,
    ScoreCopyQuality,
)


class MCPServer:
    """Lightweight MCP-like server exposing resources, tools and prompts."""

    def __init__(self) -> None:
        self.resources = load_mock_contexts()
        self.tools = {
            "generate_strategy": GenerateStrategy(),
            "generate_ads": GenerateAds(),
            "generate_seo_plan": GenerateSEOPlan(),
            "generate_crm_sequences": GenerateCRMSequences(),
            "score_copy_quality": ScoreCopyQuality(),
        }

    def list_resources(self) -> List[str]:
        return list(self.resources.keys())

    def get_resource(self, name: str) -> Any:
        rid = get_request_id()
        if name not in self.resources:
            log.warning("resource_not_found", extra=log_extra(request_id=rid, resource=name))
            raise KeyError(name)
        log.info("resource_fetched", extra=log_extra(request_id=rid, resource=name))
        return self.resources[name]

    def call_tool(
        self, name: str, payload: Dict[str, Any], request_id: str | None = None
    ) -> Dict[str, Any]:
        if name not in self.tools:
            raise KeyError(f"Tool {name} not registered")
        result = self.tools[name](payload, request_id=request_id)
        return result.model_dump() if hasattr(result, "model_dump") else dict(result)


mcp_server = MCPServer()
