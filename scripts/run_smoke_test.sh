#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${AI_METER_VENV:-$ROOT_DIR/.venv}"
PORT="${AI_METER_TEST_PORT:-8787}"
HOST="127.0.0.1"

if [ -x "$VENV_DIR/bin/ai-meter" ]; then
  export PATH="$VENV_DIR/bin:$PATH"
fi

printf '== AI Desk Meter smoke test ==\n'
command -v ai-meter >/dev/null 2>&1 || { echo 'ai-meter not found. Run scripts/install_linux_sbc.sh first.' >&2; exit 2; }

printf '\n[1/6] providers\n'
ai-meter providers

printf '\n[2/6] mock status\n'
ai-meter status --provider mock >/tmp/ai-meter-status.json
python3 -m json.tool /tmp/ai-meter-status.json >/dev/null

printf '\n[3/6] diagnostics ZIP\n'
TMP_ZIP="/tmp/ai-desk-meter-diagnostics.zip"
rm -f "$TMP_ZIP"
ai-meter diagnostics --provider mock --out "$TMP_ZIP" >/dev/null
test -s "$TMP_ZIP"

printf '\n[4/6] local API boot\n'
LOG="/tmp/ai-meter-api.log"
ai-meter serve --host "$HOST" --port "$PORT" >"$LOG" 2>&1 &
PID=$!
cleanup() { kill "$PID" >/dev/null 2>&1 || true; }
trap cleanup EXIT
sleep 1

printf '\n[5/6] /health\n'
python3 - <<PY
import json, urllib.request
with urllib.request.urlopen('http://$HOST:$PORT/health', timeout=5) as r:
    data=json.load(r)
assert data.get('ok') is True, data
print('health ok')
PY

printf '\n[6/6] /status?provider=mock\n'
python3 - <<PY
import json, urllib.request
with urllib.request.urlopen('http://$HOST:$PORT/status?provider=mock', timeout=5) as r:
    data=json.load(r)
assert data.get('schema') == 'ai-desk-meter.v1', data
print('status ok:', data.get('status'))
PY

printf '\nSmoke test passed.\n'
