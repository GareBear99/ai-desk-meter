#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_STATUS_RELATIVE = "runtime/status.json"
HOST = ROOT / "host"
if str(HOST) not in sys.path:
    sys.path.insert(0, str(HOST))

# tkinter is used by ai_meter.gui for the Catalina-safe native window with Musing state and No active Muse fallback and run_log display and cli_checker status.
from ai_meter.gui import run_gui

if __name__ == "__main__":
    raise SystemExit(run_gui(provider="mock", status_path=ROOT / DEFAULT_STATUS_RELATIVE, interval=0.5, start_runtime=True))
