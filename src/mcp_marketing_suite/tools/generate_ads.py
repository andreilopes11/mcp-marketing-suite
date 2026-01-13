from typing import Dict, List

from .base import Tool
from .schemas import AdCreative, AdsInput, AdsOutput


class GenerateAds(Tool[AdsInput, AdsOutput]):
    def __init__(self) -> None:
        super().__init__(
            name="generate_ads",
            description="Gera campanhas para Google, Meta e LinkedIn",
            input_model=AdsInput,
            output_model=AdsOutput,
        )

    def _mock_creatives(self, channel: str, payload: AdsInput) -> List[AdCreative]:
        base_headline = f"{payload.product} para {payload.audience}"
        return [
            AdCreative(
                headline=f"{base_headline} - Oferta express",
                description="Prove ROI em 30 dias com integrações prontas",
                call_to_action="Agendar demo",
                angle="Velocidade",
            ),
            AdCreative(
                headline=f"{base_headline} - Corte CAC",
                description="Analytics unificado reduz desperdício de mídia",
                call_to_action="Começar avaliação",
                angle="Eficiência",
            ),
        ]

    def run(self, payload: AdsInput, request_id: str | None = None) -> Dict:
        output = {"google": [], "meta": [], "linkedin": []}
        for channel in payload.channels:
            output[channel] = [
                creative.model_dump() for creative in self._mock_creatives(channel, payload)
            ]
        return output
