import os
import pytest

@pytest.fixture(autouse=True)
def _set_mcp_url(monkeypatch):
    # tests assume local MCP is running on default port OR is mocked by respx/httpx.
    monkeypatch.setenv("MCP_URL", os.environ.get("MCP_URL", "http://localhost:8765"))
