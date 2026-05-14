#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT/host:${PYTHONPATH:-}"

python -m compileall -q host/ai_meter
python -m pytest -q

python -m ai_meter.cli version
python -m ai_meter.cli providers
python -m ai_meter.cli doctor --provider mock >/tmp/ai-desk-meter-doctor.json
python -m ai_meter.cli status --provider mock >/tmp/ai-desk-meter-status.json
python -m ai_meter.cli companion-status --provider mock >/tmp/ai-desk-meter-companion.json
python -m ai_meter.cli diagnostics --provider mock --out /tmp/ai-desk-meter-diagnostics.zip

echo "AI Desk Meter release smoke test passed."
