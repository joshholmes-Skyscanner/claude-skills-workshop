# Orbital Travel Planner (Workshop Repo)

Backend-first Python repo designed for an **advanced Claude Code workshop**:
- agentic planning + iteration
- test-driven verification loops
- external systems mocked via **MCP server** (local + chaos)

## Quickstart

### 1) Setup (local)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e ".[dev]"
```

### 2) Run MCP (mock providers)
```bash
python -m mcp.server
```

### 3) Run API
```bash
uvicorn app.main:app --reload --port 8000
```

### 4) Try a request
```bash
curl -s http://localhost:8000/healthz | jq
curl -s -X POST http://localhost:8000/api/search \
  -H 'content-type: application/json' \
  -d '{
    "origin":"LON",
    "destination":"NYC",
    "depart_after":"2026-02-01T08:00:00Z",
    "arrive_before":"2026-02-02T08:00:00Z",
    "max_layovers": 2,
    "optimize_for":"balanced"
  }' | jq
```

### 5) Run tests
```bash
pytest -q
```

## What’s intentionally unfinished
- The core planner intentionally returns simplistic itineraries.
- Several tests are marked `xfail` to drive workshop iterations.
- Skills/agents folder is scaffolded but not wired to any specific runtime yet.

See **WORKSHOP.md** for the day agenda + exercises.
