from __future__ import annotations

from enum import Enum
from time import time
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


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


class BackendState(BaseModel):
    name: str = "none"
    receipt_state: str = "unknown"
    archive_state: str = "unknown"
    hardwire_state: str = "unknown"
    checkpoint_id: str | None = None


class UsagePayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_name: str = Field(default="ai-desk-meter.v1", alias="schema")
    service: str = "mock"
    current_percent: float = Field(default=0, ge=0, le=100)
    weekly_percent: float = Field(default=0, ge=0, le=100)
    current_reset_seconds: int = Field(default=0, ge=0)
    weekly_reset_seconds: int = Field(default=0, ge=0)
    burn_rate: BurnRate = BurnRate.normal
    status: str = Field(default="Ready", max_length=64)
    mode: MeterMode = MeterMode.active
    updated_at: int = Field(default_factory=lambda: int(time()))
    source: str = "mock"
    confidence: Confidence = Confidence.mock
    backend: BackendState | None = None
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)

    @field_validator("status")
    @classmethod
    def clean_status(cls, value: str) -> str:
        value = value.strip()
        return value or "Ready"

    @field_validator("warnings", "errors")
    @classmethod
    def clean_messages(cls, values: list[str]) -> list[str]:
        cleaned: list[str] = []
        for item in values:
            text = str(item).strip()
            if text:
                cleaned.append(text[:160])
        return cleaned[:10]

    def to_wire(self) -> dict[str, Any]:
        return self.model_dump(mode="json", by_alias=True, exclude_none=True)
