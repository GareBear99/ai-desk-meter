from __future__ import annotations

from time import time
import math

from ai_meter.protocol import BurnRate, Confidence, MeterMode, UsagePayload


class MockProvider:
    name = "mock"

    def read(self) -> UsagePayload:
        now = time()
        current = 50 + 45 * math.sin(now / 45)
        weekly = 20 + 15 * math.sin(now / 300)
        if current >= 95:
            burn = BurnRate.critical
            status = "Near limit"
        elif current >= 80:
            burn = BurnRate.high
            status = "Careful..."
        elif current <= 10:
            burn = BurnRate.low
            status = "Rested"
        else:
            burn = BurnRate.normal
            status = "✶ Musing..."
        return UsagePayload(
            service="mock-ai",
            current_percent=round(max(0, min(100, current)), 1),
            weekly_percent=round(max(0, min(100, weekly)), 1),
            current_reset_seconds=int(7200 - (now % 7200)),
            weekly_reset_seconds=int(604800 - (now % 604800)),
            burn_rate=burn,
            status=status,
            mode=MeterMode.active,
            source=self.name,
            confidence=Confidence.mock,
        )
