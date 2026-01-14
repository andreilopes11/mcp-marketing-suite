# MCP Marketing Suite

Open-source marketing copilot built on top of MCP, CrewAI, and FastAPI to orchestrate end-to-end workflows that output ads, CRM sequences, SEO plans, and strategy decks. The goal is to share my MCP stack so the community can collaborate, learn, and evolve the solution together.

## Overview
- **Purpose**: accelerate marketing deliverables with governance, traceability, and simple integration into existing pipelines.
- **Operating model**: structured inputs arrive via the MCP server or HTTP API; the CrewAI orchestrator queries contextual resources, runs deterministic tools, and stores outputs inside `outputs/`.
- **Project status**: Open alpha. Contributions are welcome—new tools, data providers, or orchestration tweaks.

## Key Capabilities
- Coordinated generation of strategy, paid media, CRM, and SEO assets from a single context payload.
- MCP server with mocked resources to simulate product, audience, brand, and competitors.
- FastAPI endpoints for synchronous trigger and retrieval of artifacts.
- Lightweight observability (JSON logs + basic tracing) so every request is inspectable.
- Langflow definition for folks who prefer adjusting the pipeline visually.

## Priority Use Cases
- **Agencies and in-house squads**: bootstrapping multi-channel campaign kits for clients or internal launches.
- **SaaS growth teams**: standardizing briefs while iterating on hypotheses and messaging.
- **Community / education**: showcasing MCP + CrewAI best practices in workshops, bootcamps, or hackathons.
- **MCP builders**: customizing tools with real inputs and contributing new public resources.

## Operating Scenarios
1. **Ads-first execution**: send product, tone, and goals to receive ready-to-use JSON for Google, Meta, and LinkedIn plus QA scoring.
2. **Full GTM playbook**: activate every channel to get strategy, SEO plan, and CRM sequences for launch squads.
3. **Deterministic mode**: run only the built-in tools (no CrewAI) for air-gapped or credential-less environments.

## Technical Limitations
- Short-lived memory per request; there is no stateful history between executions.
- Resources are mocked in memory. External connectors must be coded manually.
- No automatic LLM provider fallback if CrewAI execution fails.
- Observability is limited to logs and lightweight tracing; no prebuilt dashboards.

## Usage Limitations
- Outputs are prototypes; human review is mandatory before publishing anything.
- Tools are tuned for Portuguese or English. Other languages are not optimized.
- No native versioning for artifacts; move the final bundle to your canonical storage.

## Architecture
- **MCP server**: resources `product`, `audience`, `brand`, `competitors` plus Pydantic-validated tools.
- **CrewAI**: specialized agents coordinated by a short-term-memory orchestrator.
- **FastAPI**: exposes REST endpoints (`/api/marketing/*`, `/health`).
- **Langflow**: visual flow exported to `langflow/marketing_flow.json`.
- **Observability**: JSON logs with `request_id` correlation and spans via `observability.trace_operation`.

## Core Stack
- Python 3.11
- FastAPI + Uvicorn
- CrewAI + MCP
- Pydantic / pydantic-settings
- Ruff + Black
- Pytest
- Docker + docker-compose

## Quick Local Setup
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install .[dev]
cp .env.example .env
make run  # or: uvicorn mcp_marketing_suite.api.main:app --reload
```

### Environment Variables
- `OUTPUTS_DIR`: destination for artifacts (defaults to `outputs/`).
- `ENABLE_CREWAI`: set to `true` to call the real CrewAI stack (requires LLM creds); `false` keeps everything deterministic.

## Docker Execution
```bash
docker-compose up --build
# or
make docker-up
```

## Quick Usage Walkthrough
1. **Install & configure**: complete the local setup, add your `.env`, and decide whether CrewAI should be enabled.
2. **Start the server**: run `make run` (local) or `docker-compose up` (containerized). Confirm `GET /health` returns `200`.
3. **Prepare your context**: document product info, audience, tone, goals, and which channels you want to activate.
4. **Trigger generation**: call `POST /api/marketing/generate` or issue a MCP `createCompletion` with the same payload.
5. **Track the request**: capture the `request_id` from the response—it is the key for logs, tracing, and outputs.
6. **Collect artifacts**: download files from `outputs/<request_id>/` or call `GET /api/marketing/outputs/{request_id}`.
7. **Review & ship**: validate every asset, adapt to brand guidelines, then push to your campaign tools or CRM.

## Implementation Checklist for Any Team
1. **Decide hosting**: run locally for experimentation, containerize for CI, or deploy behind your preferred API gateway.
2. **Wire authentication**: the reference server is open; add your own auth middleware or gateway rules before exposing it.
3. **Integrate data sources**: replace the mocked resources in `resources/context_data.py` with calls to your CMS, CDP, or BI endpoints.
4. **Embed in pipelines**:
   - **Automation**: create a CI step that posts briefs to `/api/marketing/generate` and commits the resulting bundle to Git.
   - **Product workflows**: from a design system or PM tool, trigger the MCP server through webhooks and store the `request_id` back in the ticket.
   - **Agentic apps**: plug the MCP server as a tool in your broader MCP network so other agents can call marketing outputs on demand.
5. **Observability**: forward logs to your stack (ELK, OpenSearch, Splunk). The `request_id` makes correlation trivial.
6. **Governance**: define review checkpoints so no asset goes live without human sign-off.

## HTTP Endpoints
- `POST /api/marketing/generate`
  ```json
  {
    "product": "Acme Analytics",
    "audience": "SaaS CMOs",
    "brand": "Consultative and direct tone",
    "goals": ["Lower CAC", "Increase LTV"],
    "ad_channels": ["google", "meta", "linkedin"],
    "crm_channels": ["email", "whatsapp"]
  }
  ```
  Returns `{ "request_id": "...", "output_dir": "outputs/<id>" }`.
- `GET /api/marketing/outputs/{request_id}`: lists the files generated for the given run.
- `GET /health`: liveness probe.

## Generated Artifacts
Each `request_id` creates files inside `outputs/<id>/`:
- `strategy.md`
- `ads_google.json`
- `ads_meta.json`
- `ads_linkedin.json`
- `seo_plan.md`
- `crm_sequences.json`
- `qa_report.md`
- `final_bundle.json`

## Langflow
Import `langflow/marketing_flow.json` into Langflow to visualize or edit the pipeline: structured inputs, MCP resource lookups, crew execution, and fan-out of artifacts.

## Observability
- JSON logs via `python-json-logger` with `request_id` correlation.
- `observability.trace_operation` adds lightweight spans around tools and agents.

## Repository Structure
- `src/mcp_marketing_suite/`: core package
- `.../api/`: FastAPI app
- `.../crew/`: orchestrator + agents
- `.../tools/`: MCP tools and schemas
- `.../prompts/`: versioned prompts
- `.../resources/`: mocks and contextual data
- `langflow/`: visual flow definition
- `outputs/`: generated artifacts

## Testing & Quality
```bash
make lint
make format
make test
```

## Community & Contribution
- Open-source MCP-first mindset—PRs, issues, and new tool ideas are welcome.
- Suggest integrations (real CRM, BI feeds, distributed storage) through issues so we can discuss design.
- Share real-world cases, report bugs, and document limitations you hit so we can iterate faster as a community.

## curl Examples
```bash
curl -X POST http://localhost:8000/api/marketing/generate \
  -H "Content-Type: application/json" \
  -d '{"product":"Acme","audience":"CMO","brand":"Direct","goals":["ROI"]}'

curl http://localhost:8000/api/marketing/outputs/<request_id>
```
