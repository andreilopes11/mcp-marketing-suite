from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, Tuple

from pydantic import BaseModel, ConfigDict, Field, field_validator

_DEFAULT_AD_CHANNELS = ["google", "meta", "linkedin"]
_DEFAULT_CRM_CHANNELS = ["email", "whatsapp", "sms"]


class GenerateRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    product: str
    audience: str
    brand: str
    goals: List[str] = Field(default_factory=list)
    offers: List[str] = Field(default_factory=list)
    seo_theme: Optional[str] = None
    ad_channels: Tuple[Literal["google", "meta", "linkedin"], ...] = Field(
        default_factory=lambda: tuple(_DEFAULT_AD_CHANNELS)
    )
    crm_channels: Tuple[Literal["email", "whatsapp", "sms"], ...] = Field(
        default_factory=lambda: tuple(_DEFAULT_CRM_CHANNELS)
    )

    def _base_payload(self) -> Dict[str, Any]:
        return {
            "product": self.product,
            "audience": self.audience,
            "brand": self.brand,
            "goals": list(self.goals),
        }

    @field_validator("product", "audience", "brand", mode="before")
    @classmethod
    def _validate_non_empty(cls, value: str) -> str:
        if not value or not str(value).strip():
            raise ValueError("Campo obrigatório não pode ser vazio")
        return str(value).strip()

    def strategy_payload(self) -> Dict[str, Any]:
        return self._base_payload()

    def ads_payload(self) -> Dict[str, Any]:
        payload = self._base_payload()
        payload.update({"channels": list(self.ad_channels), "offers": list(self.offers)})
        return payload

    def seo_payload(self) -> Dict[str, Any]:
        payload = self._base_payload()
        if self.seo_theme:
            payload["theme"] = self.seo_theme
        return payload

    def crm_payload(self) -> Dict[str, Any]:
        payload = self._base_payload()
        payload["channels"] = list(self.crm_channels)
        return payload

    def as_dict(self) -> Dict[str, Any]:
        return {
            **self._base_payload(),
            "offers": list(self.offers),
            "ad_channels": list(self.ad_channels),
            "crm_channels": list(self.crm_channels),
            "seo_theme": self.seo_theme,
        }
