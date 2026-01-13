PYTHON=python
APP=mcp_marketing_suite

.PHONY: install dev lint format test run docker-build docker-up docker-down

install:
	$(PYTHON) -m pip install --upgrade pip
	pip install .

dev:
	pip install .[dev]

lint:
	ruff check src tests

format:
	black src tests

format-check:
	black --check src tests

test:
	pytest -q

run:
	uvicorn $(APP).api.main:app --host 0.0.0.0 --port 8000 --reload

docker-build:
	docker build -t $(APP):latest .

docker-up:
	docker-compose up --build

docker-down:
	docker-compose down
