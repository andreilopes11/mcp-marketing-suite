from crewai import Agent

from ..observability import get_request_id

SYSTEM_PROMPT = (
    "Você é um especialista de marketing B2B SaaS. Seja conciso e entregue ação."  # noqa: E501
)


def make_agent(role: str, goal: str, backstory: str) -> Agent:
    return Agent(role=role, goal=goal, backstory=backstory, verbose=False, allow_delegation=False)


MarketResearchAnalyst = lambda: make_agent(  # noqa: E731
    role="MarketResearchAnalyst",
    goal="Produzir ICP e proposta de valor",
    backstory="Pesquisa tendências e concorrentes para gerar posicionamento",
)

Copywriter = lambda: make_agent(  # noqa: E731
    role="Copywriter",
    goal="Criar copies persuasivas multicanal",
    backstory="Especialista em anúncios de performance",
)

PerformanceMarketer = lambda: make_agent(  # noqa: E731
    role="PerformanceMarketer",
    goal="Planejar campanhas pagas com ROI",
    backstory="Focado em testes e otimização",
)

SEOPlanner = lambda: make_agent(  # noqa: E731
    role="SEOPlanner",
    goal="Desenhar clusters e calendário SEO",
    backstory="Especialista em conteúdo orgânico e SERP",
)

CRMStrategist = lambda: make_agent(  # noqa: E731
    role="CRMStrategist",
    goal="Construir sequências e segmentação",
    backstory="Foco em engajamento e retenção",
)

QAComplianceReviewer = lambda: make_agent(  # noqa: E731
    role="QAComplianceReviewer",
    goal="Checar coerência e compliance de marketing",
    backstory="Garante clareza e evita claims não suportados",
)


AGENT_BUILDERS = [
    MarketResearchAnalyst,
    Copywriter,
    PerformanceMarketer,
    SEOPlanner,
    CRMStrategist,
    QAComplianceReviewer,
]
