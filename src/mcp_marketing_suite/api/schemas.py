"""API schemas.

These re-export the canonical models defined in ``mcp_marketing_suite.models`` to avoid
duplicated definitions between the API layer and the orchestration layer.
"""

from ..models import GenerateRequest

__all__ = ["GenerateRequest"]
