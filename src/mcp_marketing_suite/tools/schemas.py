from typing import List, Literal, Optional

from pydantic import BaseModel, Field, ConfigDict


class StrategyInput(BaseModel):
    product: str
    audience: str
    brand: str
    goals: List[str] = Field(default_factory=list)


class StrategyOutput(BaseModel):
    icp: str
    value_proposition: str
    differentiators: List[str]
    channel_mix: dict
    narrative: str


class AdsInput(BaseModel):
    product: str
    audience: str
    brand: str
    channels: List[Literal["google", "meta", "linkedin"]]
    offers: List[str] = Field(default_factory=list)


class AdCreative(BaseModel):
    headline: str
    description: str
    call_to_action: str
    angle: str


class AdsOutput(BaseModel):
    google: List[AdCreative]
    meta: List[AdCreative]
    linkedin: List[AdCreative]


class SEOPlanInput(BaseModel):
    product: str
    audience: str
    brand: str
    theme: Optional[str] = None


class SEOCluster(BaseModel):
    cluster: str
    keywords: List[str]
    outline: List[str]


class SEOPlanOutput(BaseModel):
    clusters: List[SEOCluster]
    calendar: List[str]
    briefs: List[str]


class CRMSequencesInput(BaseModel):
    product: str
    audience: str
    brand: str
    channels: List[Literal["email", "whatsapp", "sms"]]


class CRMSequence(BaseModel):
    channel: str
    steps: List[str]
    segmentation: str


class CRMSequencesOutput(BaseModel):
    sequences: List[CRMSequence]


class CopyScoreInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    copy_text: str = Field(alias="copy")
    context: Optional[str] = None


class CopyScoreOutput(BaseModel):
    score: int = Field(ge=0, le=100)
    feedback: List[str]
