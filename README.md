# MCP Marketing Suite

Marketing Copilot que expõe um MCP server, orquestração CrewAI e endpoints FastAPI para gerar entregáveis de marketing.

## Arquitetura
- **MCP server**: resources mockados (product/audience/brand/competitors) e tools com validação via Pydantic.
- **CrewAI**: agentes especializados executados por um orchestrator com memória curta por request.
- **Langflow**: fluxo visual exportado em `langflow/marketing_flow.json`.
- **FastAPI**: endpoints HTTP para disparar e recuperar outputs.
- **Observabilidade**: logs estruturados (JSON), correlação por `request_id`, tracing básico.

## Stack
- Python 3.11
- FastAPI + Uvicorn
- CrewAI
- MCP interface interna
- Pydantic / pydantic-settings
- Ruff + Black
- Pytest
- Docker + docker-compose

## Setup local
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install --upgrade pip
pip install .[dev]
cp .env.example .env
make run  # ou: uvicorn mcp_marketing_suite.api.main:app --reload
```

## Endpoints
- `POST /api/marketing/generate`
  - Body exemplo:
    ```json
    {
      "product": "Acme Analytics",
      "audience": "CMOs de SaaS",
      "brand": "Tom consultivo e direto",
      "goals": ["Reduzir CAC", "Aumentar LTV"]
    }
    ```
  - Retorno: `{ "request_id": "...", "output_dir": "outputs/<id>" }`
- `GET /api/marketing/outputs/{request_id}`: retorna arquivos do request.
- `GET /health`: status simples.

## Pipeline / Saídas
Para cada `request_id` em `outputs/<id>/`:
- strategy.md
- ads_google.json
- ads_meta.json
- ads_linkedin.json
- seo_plan.md
- crm_sequences.json
- qa_report.md
- final_bundle.json

## Docker
```bash
docker-compose up --build
# ou
make docker-up
```

## Langflow
Abra o Langflow e importe `langflow/marketing_flow.json`. O fluxo contém nós de input, consulta aos resources MCP, execução do crew e saída dos artefatos.

## Testes e qualidade
```bash
make lint
make format
make test
```

## Mocking de resources
Os resources MCP são mockados em memória em `mcp_marketing_suite/resources/context_data.py`. Ajuste conforme necessidade ou integre fontes externas sem alterar as tools.

## Observabilidade
- Logs em JSON via `python-json-logger` com `request_id`.
- Tracing leve via `observability.trace_operation`.

## Estrutura
- `src/mcp_marketing_suite/` pacote principal
- `src/mcp_marketing_suite/tools/` tools MCP com schemas
- `src/mcp_marketing_suite/crew/` orchestrator + agentes
- `src/mcp_marketing_suite/api/` app FastAPI
- `src/mcp_marketing_suite/prompts/` prompts versionados
- `langflow/` fluxo visual
- `outputs/` artefatos gerados

## Exemplos de uso via curl
```bash
curl -X POST http://localhost:8000/api/marketing/generate \
  -H "Content-Type: application/json" \
  -d '{"product":"Acme","audience":"CMO","brand":"Direto","goals":["ROI"]}'

curl http://localhost:8000/api/marketing/outputs/<request_id>
```
