from typing import Any, Dict

from ..mcp_server import mcp_server
from ..observability import get_request_id


class MCPClient:
    """Thin wrapper to call MCP resources and tools."""

    def get_resource(self, name: str) -> Any:
        return mcp_server.get_resource(name)

    def call_tool(self, name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return mcp_server.call_tool(name, payload, request_id=get_request_id())


def get_client() -> MCPClient:
    return MCPClient()
