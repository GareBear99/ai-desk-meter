from __future__ import annotations

from time import time
from datetime import datetime
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
        elif current >= 80:
            burn = BurnRate.high
        elif current <= 10:
            burn = BurnRate.low
        else:
            burn = BurnRate.normal
        # Mock means the runtime/CLI writer is alive. It is not a real Muse/model
        # connection, so the UI must keep showing No active Muse while the
        # top-right runtime connection dot can still be green.
        status = "No active Muse"
        stamp = datetime.fromtimestamp(now).strftime("%H:%M:%S")
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
            runtime_connected=True,
            muse_connected=False,
            muse_state="none",
            last_action="mock runtime payload refreshed",
            action_in_progress="none",
            cli_checker={
                "state": "active",
                "last_check": int(now),
                "message": "mock provider sampled successfully",
            },
            run_log=[
                f"[{stamp}] status payload loaded",
                f"[{stamp}] provider mock updated",
                f"[{stamp}] runtime connected; no active Muse",
            ],
        )
