from typing import Dict, List

from .base import Tool
from .schemas import CRMSequence, CRMSequencesInput, CRMSequencesOutput


class GenerateCRMSequences(Tool[CRMSequencesInput, CRMSequencesOutput]):
    def __init__(self) -> None:
        super().__init__(
            name="generate_crm_sequences",
            description="Gera sequências de CRM para email, WhatsApp e SMS",
            input_model=CRMSequencesInput,
            output_model=CRMSequencesOutput,
        )

    def _sequence(self, channel: str, payload: CRMSequencesInput) -> CRMSequence:
        steps = [
            "Dia 0: mensagem de valor + prova social",
            "Dia 3: estudo de caso",
            "Dia 7: oferta com CTA",
        ]
        return CRMSequence(
            channel=channel, steps=steps, segmentation=f"Segmento: {payload.audience}"
        )

    def run(self, payload: CRMSequencesInput, request_id: str | None = None) -> Dict:
        sequences: List[Dict] = []
        for channel in payload.channels:
            sequences.append(self._sequence(channel, payload).model_dump())
        return {"sequences": sequences}
