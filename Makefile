.PHONY: install run-mcp run-api test lint

install:
	pip install -e ".[dev]"

run-mcp:
	python -m mcp.server

run-api:
	uvicorn app.main:app --reload --port 8000

test:
	pytest -q

lint:
	ruff check .
