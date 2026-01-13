import json
from pathlib import Path
from typing import Any, Dict, List

from crewai import Crew, Task

from ..logging_config import log, log_extra
from ..observability import get_request_id, trace_operation
from ..tools import (
    GenerateAds,
    GenerateCRMSequences,
    GenerateSEOPlan,
    GenerateStrategy,
    ScoreCopyQuality,
)
from .agents import AGENT_BUILDERS
from .client import MCPClient, get_client


class MarketingOrchestrator:
    """Creates tasks per request and executes them in order using CrewAI."""

    def __init__(self, mcp_client: MCPClient | None = None) -> None:
        self.mcp_client = mcp_client or get_client()
        self.tools = {
            "generate_strategy": GenerateStrategy(),
            "generate_ads": GenerateAds(),
            "generate_seo_plan": GenerateSEOPlan(),
            "generate_crm_sequences": GenerateCRMSequences(),
            "score_copy_quality": ScoreCopyQuality(),
        }

    def _build_tasks(self, payload: Dict[str, Any]) -> List[Task]:
        tasks: List[Task] = []
        request_id = get_request_id()

        # Strategy
        tasks.append(
            Task(
                description="Gerar estratégia e posicionamento",
                expected_output="JSON com icp, value_proposition, differentiators, channel_mix, narrative",
                agent=AGENT_BUILDERS[0](),
                tools=[self.tools["generate_strategy"]],
            )
        )
        # Ads
        tasks.append(
            Task(
                description="Gerar campanhas para Google, Meta e LinkedIn",
                expected_output="JSON com criativos por canal",
                agent=AGENT_BUILDERS[1](),
                tools=[self.tools["generate_ads"], self.tools["score_copy_quality"]],
            )
        )
        # SEO
        tasks.append(
            Task(
                description="Gerar plano SEO",
                expected_output="Clusters, calendário e briefs",
                agent=AGENT_BUILDERS[3](),
                tools=[self.tools["generate_seo_plan"]],
            )
        )
        # CRM
        tasks.append(
            Task(
                description="Gerar sequências CRM",
                expected_output="Sequências por canal",
                agent=AGENT_BUILDERS[4](),
                tools=[self.tools["generate_crm_sequences"]],
            )
        )
        # QA
        tasks.append(
            Task(
                description="Revisar compliance e coerência",
                expected_output="Markdown com riscos e sugestões",
                agent=AGENT_BUILDERS[5](),
                tools=[self.tools["score_copy_quality"]],
            )
        )
        log.info("tasks_built", extra=log_extra(request_id=request_id, task_count=len(tasks)))
        return tasks

    def run(self, payload: Dict[str, Any], output_dir: Path) -> Dict[str, Any]:
        rid = get_request_id()
        with trace_operation("orchestrator_run", request_id=rid):
            tasks = self._build_tasks(payload)
            crew = Crew(
                agents=[builder() for builder in AGENT_BUILDERS], tasks=tasks, verbose=False
            )
            results = crew.kickoff()

            bundle = {
                "strategy": self.tools["generate_strategy"](payload, request_id=rid),
                "ads": self.tools["generate_ads"](payload, request_id=rid),
                "seo": self.tools["generate_seo_plan"](payload, request_id=rid),
                "crm": self.tools["generate_crm_sequences"](payload, request_id=rid),
                "qa": {"feedback": "Mock QA - checar claims e fontes"},
            }

            output_dir.mkdir(parents=True, exist_ok=True)
            (output_dir / "strategy.md").write_text(
                json.dumps(bundle["strategy"].model_dump(), indent=2), encoding="utf-8"
            )
            (output_dir / "ads_google.json").write_text(
                json.dumps(bundle["ads"]["google"], indent=2), encoding="utf-8"
            )
            (output_dir / "ads_meta.json").write_text(
                json.dumps(bundle["ads"]["meta"], indent=2), encoding="utf-8"
            )
            (output_dir / "ads_linkedin.json").write_text(
                json.dumps(bundle["ads"]["linkedin"], indent=2), encoding="utf-8"
            )
            (output_dir / "seo_plan.md").write_text(
                json.dumps(bundle["seo"], indent=2), encoding="utf-8"
            )
            (output_dir / "crm_sequences.json").write_text(
                json.dumps(bundle["crm"], indent=2), encoding="utf-8"
            )
            (output_dir / "qa_report.md").write_text("QA mock report", encoding="utf-8")
            (output_dir / "final_bundle.json").write_text(
                json.dumps(
                    bundle, default=lambda o: getattr(o, "model_dump", lambda: o)(), indent=2
                ),
                encoding="utf-8",
            )

            log.info("outputs_written", extra=log_extra(request_id=rid, path=str(output_dir)))
            return {"request_id": rid, "output_dir": str(output_dir), "bundle": bundle}


def get_orchestrator() -> MarketingOrchestrator:
    return MarketingOrchestrator()
