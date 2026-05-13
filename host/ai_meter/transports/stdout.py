from __future__ import annotations

import json

from ai_meter.protocol import UsagePayload


class StdoutTransport:
    name = "stdout"

    def send(self, payload: UsagePayload) -> None:
        print(json.dumps(payload.to_wire(), separators=(",", ":")))
