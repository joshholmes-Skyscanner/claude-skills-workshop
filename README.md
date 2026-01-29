# Orbital Travel Planner

A full-stack travel planning application with a Python FastAPI backend and vanilla JavaScript frontend. This project demonstrates:
- Multi-leg itinerary search and optimization
- External systems mocked via **MCP server** (local + chaos mode)
- Test-driven development with pytest
- Clean architecture with domain-driven design

## Quick Start

### Prerequisites
- Python 3.11+
- pip

### 1) Installation

Clone the repository and set up the Python environment:

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -U pip
pip install -e ".[dev]"
```

### 2) Start the MCP Server (Required)

The MCP server provides mock travel provider data. Start it in a **separate terminal**:

```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python -m mcp.server
```

Leave this running - the API depends on it.

### 3) Start the API Server

In another terminal, start the FastAPI server:

```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

### 4) Access the Application

Open your browser and navigate to:

**http://localhost:8000**

You'll see the Orbital Travel Planner web interface where you can:
- Search for travel routes between cities
- Specify time windows for departure and arrival
- Choose optimization preferences (fastest, cheapest, greenest, balanced)
- View detailed itineraries with multiple legs

### 5) Test with cURL (Optional)

Test the health endpoint:
```bash
curl -s http://localhost:8000/healthz | jq
```

Test the search API directly:
```bash
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

### 6) Run Tests

```bash
pytest -q
```

For verbose output with coverage:
```bash
pytest -v --cov=app
```

## Project Structure

```
orbital-travel-planner/
├── app/
│   ├── api/          # FastAPI route handlers
│   ├── domain/       # Business logic and models
│   ├── services/     # External service clients (MCP, planner)
│   ├── static/       # Frontend files (HTML, CSS, JS)
│   ├── main.py       # FastAPI application entry point
│   └── models.py     # Pydantic models for API
├── mcp/              # Mock MCP server for provider data
├── tests/            # Test suite
├── pyproject.toml    # Python dependencies and config
└── README.md         # This file
```

## API Endpoints

### GET /
Serves the frontend web application

### GET /healthz
Health check endpoint
- **Response**: `{"ok": true}`

### POST /api/search
Search for travel itineraries
- **Request Body**:
  ```json
  {
    "origin": "LON",
    "destination": "NYC",
    "depart_after": "2026-02-01T08:00:00Z",
    "arrive_before": "2026-02-02T08:00:00Z",
    "max_layovers": 2,
    "optimize_for": "balanced"
  }
  ```
- **optimize_for options**: `fastest`, `cheapest`, `greenest`, `balanced`
- **Response**: List of travel plans with legs, metrics, and scores

## Development

### Running in Development Mode

The application uses `--reload` flag with uvicorn, which automatically restarts the server when code changes are detected.

### Code Quality

Run linting and type checking:
```bash
ruff check .
mypy app/
```

## Troubleshooting

**Q: I get "Internal Server Error" when searching**
- Make sure the MCP server is running in a separate terminal (`python -m mcp.server`)
- Check that both servers are using the expected ports (MCP: default, API: 8000)

**Q: The frontend doesn't load**
- Verify the API server is running on port 8000
- Check the browser console for errors
- Ensure `app/static/` directory exists with the frontend files

**Q: Tests are failing**
- Make sure you installed dev dependencies: `pip install -e ".[dev]"`
- Some tests may be marked `xfail` intentionally for workshop exercises

## What's Intentionally Unfinished

This project is designed for learning and workshops:
- The core planner returns simplified itineraries
- Several tests are marked `xfail` to drive iterations
- The MCP server includes a "chaos mode" for testing error handling

See **WORKSHOP.md** for the workshop agenda and exercises.
