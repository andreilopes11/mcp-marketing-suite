# syntax=docker/dockerfile:1.6
FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=1.7.1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md /app/
COPY src /app/src
COPY langflow /app/langflow
COPY outputs /app/outputs

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .[dev]

EXPOSE 8000
CMD ["uvicorn", "mcp_marketing_suite.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
