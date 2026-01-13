from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, TypeVar

from pydantic import BaseModel, ValidationError

from ..logging_config import log, log_extra

InputModel = TypeVar("InputModel", bound=BaseModel)
OutputModel = TypeVar("OutputModel", bound=BaseModel)


class ToolExecutionError(Exception):
    """Raised when a tool fails after validation."""


class Tool(ABC, Generic[InputModel, OutputModel]):
    name: str
    description: str
    input_model: type[InputModel]
    output_model: type[OutputModel]

    def __init__(
        self,
        name: str,
        description: str,
        input_model: type[InputModel],
        output_model: type[OutputModel],
    ):
        self.name = name
        self.description = description
        self.input_model = input_model
        self.output_model = output_model

    def __call__(self, payload: Dict[str, Any], request_id: str | None = None) -> OutputModel:
        try:
            validated_input = self.input_model(**payload)
        except ValidationError as exc:  # noqa: TRY003
            log.error(
                "validation_error",
                extra=log_extra(request_id=request_id, tool=self.name, errors=exc.errors()),
            )
            raise

        try:
            result = self.run(validated_input, request_id=request_id)
            if not isinstance(result, self.output_model):
                result = self.output_model(**result)  # type: ignore[arg-type]
            log.info("tool_success", extra=log_extra(request_id=request_id, tool=self.name))
            return result
        except Exception as exc:  # noqa: BLE001
            log.exception("tool_failure", extra=log_extra(request_id=request_id, tool=self.name))
            raise ToolExecutionError(str(exc))

    @abstractmethod
    def run(
        self, payload: InputModel, request_id: str | None = None
    ) -> OutputModel | Dict[str, Any]:
        raise NotImplementedError
