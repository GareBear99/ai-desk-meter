from __future__ import annotations

from enum import Enum
from time import time
from typing import Any

from pydantic import BaseModel, Field, field_validator


class BurnRate(str, Enum):
    idle = "idle"
    low = "low"
    normal = "normal"
    high = "high"
    critical = "critical"


class MeterMode(str, Enum):
    boot = "boot"
    pairing = "pairing"
    active = "active"
    stale = "stale"
    offline = "offline"
    error = "error"
    demo = "demo"


class Confidence(str, Enum):
    exact = "exact"
    estimated = "estimated"
    mock = "mock"
    unknown = "unknown"


class UsagePayload(BaseModel):
    schema: str = "ai-desk-meter.v1"
    service: str = "mock"
    current_percent: float = Field(ge=0, le=100)
    weekly_percent: float = Field(ge=0, le=100)
    current_reset_seconds: int = Field(ge=0)
    weekly_reset_seconds: int = Field(ge=0)
    burn_rate: BurnRate = BurnRate.normal
    status: str = Field(default="Musing...", max_length=48)
    mode: MeterMode = MeterMode.active
    updated_at: int = Field(default_factory=lambda: int(time()))
    source: str = "mock"
    confidence: Confidence = Confidence.mock

    @field_validator("status")
    @classmethod
    def clean_status(cls, value: str) -> str:
        value = value.strip()
        return value or "Ready"

    def to_wire(self) -> dict[str, Any]:
        return self.model_dump(mode="json")
