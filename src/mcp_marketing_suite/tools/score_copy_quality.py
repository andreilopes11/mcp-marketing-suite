from .base import Tool
from .schemas import CopyScoreInput, CopyScoreOutput


class ScoreCopyQuality(Tool[CopyScoreInput, CopyScoreOutput]):
    def __init__(self) -> None:
        super().__init__(
            name="score_copy_quality",
            description="Pontua copy e retorna feedbacks",
            input_model=CopyScoreInput,
            output_model=CopyScoreOutput,
        )

    def run(self, payload: CopyScoreInput, request_id: str | None = None) -> CopyScoreOutput:
        score = min(100, 60 + len(payload.copy_text) % 40)
        feedback = [
            "Consistência com posicionamento da marca",
            "Clareza do call-to-action",
        ]
        if payload.context:
            feedback.append(f"Contexto considerado: {payload.context[:80]}")
        return CopyScoreOutput(score=score, feedback=feedback)
