from typing import Dict

from .base import Tool
from .schemas import SEOCluster, SEOPlanInput, SEOPlanOutput


class GenerateSEOPlan(Tool[SEOPlanInput, SEOPlanOutput]):
    def __init__(self) -> None:
        super().__init__(
            name="generate_seo_plan",
            description="Cria clusters, calendário e briefs SEO",
            input_model=SEOPlanInput,
            output_model=SEOPlanOutput,
        )

    def run(self, payload: SEOPlanInput, request_id: str | None = None) -> Dict:
        clusters = [
            SEOCluster(
                cluster="Analytics de Marketing",
                keywords=["marketing analytics", "dashboard marketing", "atribuição de marketing"],
                outline=["O que é", "Benefícios", "Como implementar"],
            ),
            SEOCluster(
                cluster="CAC e LTV",
                keywords=["reduzir CAC", "aumentar LTV", "previsão de receita"],
                outline=["Modelos", "Métricas", "Ferramentas"],
            ),
        ]
        calendar = ["Semana 1: Cluster Analytics", "Semana 2: Cluster CAC/LTV"]
        briefs = [
            "Artigo 1: como unificar dados de mídia e CRM",
            "Artigo 2: framework para medir LTV por canal",
        ]
        return {
            "clusters": [c.model_dump() for c in clusters],
            "calendar": calendar,
            "briefs": briefs,
        }
