from __future__ import annotations

from ai_meter.protocol import BurnRate, Confidence, MeterMode, UsagePayload


class ManualProvider:
    name = "manual"

    def read(self) -> UsagePayload:
        return UsagePayload(
            service="manual",
            current_percent=0,
            weekly_percent=0,
            current_reset_seconds=0,
            weekly_reset_seconds=0,
            burn_rate=BurnRate.idle,
            status="Manual mode",
            mode=MeterMode.active,
            source=self.name,
            confidence=Confidence.estimated,
        )
