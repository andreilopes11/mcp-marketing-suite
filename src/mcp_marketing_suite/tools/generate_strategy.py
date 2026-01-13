from typing import Dict

from .base import Tool
from .schemas import StrategyInput, StrategyOutput


class GenerateStrategy(Tool[StrategyInput, StrategyOutput]):
    def __init__(self) -> None:
        super().__init__(
            name="generate_strategy",
            description="Gera estratégia e posicionamento marketing",
            input_model=StrategyInput,
            output_model=StrategyOutput,
        )

    def run(self, payload: StrategyInput, request_id: str | None = None) -> Dict:
        differentiators = [
            f"Enfatizar {payload.product} como líder em velocidade",
            "Provar ROI com casos de uso por vertical",
            "Usar tom " + payload.brand,
        ]
        channel_mix = {
            "paid": ["Google Search", "Meta Retargeting", "LinkedIn ABM"],
            "organic": ["SEO clusters", "Webinars", "Newsletter"],
        }
        narrative = (
            f"Para {payload.audience}, {payload.product} entrega resultados medíveis "
            "e reduz complexidade operacional."
        )
        return {
            "icp": payload.audience,
            "value_proposition": f"{payload.product} resolve {', '.join(payload.goals or ['os principais desafios'])}",
            "differentiators": differentiators,
            "channel_mix": channel_mix,
            "narrative": narrative,
        }
