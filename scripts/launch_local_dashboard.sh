#!/usr/bin/env bash
set -euo pipefail

HOST="${AI_METER_HOST:-127.0.0.1}"
PORT="${AI_METER_PORT:-8787}"
PROVIDER="${AI_METER_PROVIDER:-mock}"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Starting AI Desk Meter local API on http://${HOST}:${PORT}"
echo "Default provider: ${PROVIDER}"

cd "${ROOT_DIR}/host"
if ! command -v ai-meter >/dev/null 2>&1; then
  echo "ai-meter command not found; installing host package in editable mode"
  python3 -m pip install -e .
fi

python3 -m ai_meter.cli serve --host "${HOST}" --port "${PORT}"
