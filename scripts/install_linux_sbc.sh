#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOST_DIR="$ROOT_DIR/host"
VENV_DIR="${AI_METER_VENV:-$ROOT_DIR/.venv}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

printf '== AI Desk Meter Linux/SBC install ==\n'
printf 'Root: %s\n' "$ROOT_DIR"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Missing python3. Install Python 3.10+ first." >&2
  exit 2
fi

"$PYTHON_BIN" - <<'PY'
import sys
if sys.version_info < (3, 10):
    raise SystemExit('Python 3.10+ is required')
print('Python OK:', sys.version.split()[0])
PY

"$PYTHON_BIN" -m venv "$VENV_DIR"
# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip
python -m pip install -e "$HOST_DIR"

printf '\nInstalled ai-meter into %s\n' "$VENV_DIR"
printf 'Try:\n  source %s/bin/activate\n  ai-meter providers\n  ai-meter status --provider mock\n  ai-meter serve --host 127.0.0.1 --port 8787\n' "$VENV_DIR"
