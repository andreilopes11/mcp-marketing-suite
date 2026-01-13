from dataclasses import dataclass, field
from typing import List


@dataclass
class ProductContext:
    name: str
    description: str
    price_positioning: str
    benefits: List[str] = field(default_factory=list)


@dataclass
class AudienceContext:
    segment: str
    pains: List[str]
    goals: List[str]
    decision_criteria: List[str]


@dataclass
class BrandContext:
    tone: str
    proof_points: List[str]
    values: List[str]


@dataclass
class CompetitorsContext:
    names: List[str]
    differentiators: List[str]


def load_mock_contexts() -> dict:
    return {
        "product_context": ProductContext(
            name="Acme Analytics",
            description="Plataforma SaaS de marketing analytics com dashboards plug-and-play",
            price_positioning="premium",
            benefits=[
                "Implementação em 1 semana",
                "Modelos preditivos para CAC e LTV",
                "Integrações nativas com Google, Meta e CRM",
            ],
        ),
        "audience_context": AudienceContext(
            segment="Heads de Marketing de empresas digitais",
            pains=["Pressão por ROI", "Dados fragmentados", "Dependência de BI"],
            goals=["Reduzir CAC", "Aumentar LTV", "Ganhar velocidade em mídia"],
            decision_criteria=["Prova de ROI", "Segurança de dados", "Facilidade de integração"],
        ),
        "brand_context": BrandContext(
            tone="Consultivo, direto, com autoridade técnica",
            proof_points=["+120 clientes enterprise", "ISO 27001", "Parceiro Google Premier"],
            values=["Transparência", "Velocidade", "Foco em negócio"],
        ),
        "competitors_context": CompetitorsContext(
            names=["Datasight", "Metricly"],
            differentiators=["Automação de insights", "Time de estrategistas dedicado"],
        ),
    }
