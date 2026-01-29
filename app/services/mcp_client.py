from __future__ import annotations

from typing import Any
import os
import httpx

class MCPClient:
    """Tiny MCP-ish client for the workshop.

    We model tools as HTTP endpoints:
      POST {MCP_URL}/tools/<tool_name>
    with JSON in/out.

    This is intentionally small so you can swap it later for a proper MCP client/runtime.
    """

    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = base_url or os.environ.get("MCP_URL", "http://localhost:8765")

    async def call(self, tool: str, payload: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base_url}/tools/{tool}"
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.post(url, json=payload)
            r.raise_for_status()
            return r.json()
