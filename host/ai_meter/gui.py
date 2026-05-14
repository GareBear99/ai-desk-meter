from __future__ import annotations

import json
import random
import threading
import time
from pathlib import Path
from typing import Any

from ai_meter.writer import write_status

NO_ACTIVE_MUSE = "No active Muse"
SVG_NO_MUSE = "No Muse."


def _safe_number(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


class RuntimeWriter:
    """Background no-server runtime writer used by the one-command GUI."""

    def __init__(self, *, provider: str, path: Path, interval: float) -> None:
        self.provider = provider
        self.path = Path(path)
        self.interval = max(0.1, float(interval))
        self._stop = threading.Event()
        self.thread: threading.Thread | None = None

    def start(self) -> None:
        if self.thread and self.thread.is_alive():
            return
        self.thread = threading.Thread(target=self._run, name="ai-meter-runtime-writer", daemon=True)
        self.thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)

    def _run(self) -> None:
        while not self._stop.is_set():
            try:
                write_status(self.path, self.provider)
            except Exception:
                # GUI will show No active Muse / file error if write fails.
                pass
            self._stop.wait(self.interval)


class TkMuseApp:
    """Native Tk no-server GUI. No localhost server and no Tauri requirement."""

    def __init__(self, root, *, provider: str, status_path: Path, interval: float, start_runtime: bool = True) -> None:
        import tkinter as tk
        from tkinter import font

        self.tk = tk
        self.root = root
        self.provider = provider
        self.status_path = Path(status_path)
        self.refresh_ms = max(100, int(float(interval) * 1000))
        self.runtime_writer = RuntimeWriter(provider=provider, path=self.status_path, interval=interval) if start_runtime else None
        self.dot_count = 0
        self.eye_closed = False
        self.connected = False
        self.is_musing = False
        self.next_blink = time.time() + random.uniform(3, 11)
        self.blink_until = 0.0
        self.title_font = font.Font(family="Helvetica", size=42, weight="bold")
        self.card_font = font.Font(family="Helvetica", size=22, weight="bold")
        self.small_font = font.Font(family="Menlo", size=11)

        self.root.title("AI Desk Meter")
        self.root.geometry("960x680")
        self.root.configure(bg="#05070b")
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.build()
        if self.runtime_writer:
            self.runtime_writer.start()
        self.tick()

    def build(self) -> None:
        tk = self.tk
        hero = tk.Frame(self.root, bg="#0a0e17", highlightbackground="#263247", highlightthickness=1)
        hero.pack(fill="x", padx=24, pady=24)
        self.canvas = tk.Canvas(hero, width=190, height=140, bg="#05070b", highlightthickness=0)
        self.canvas.pack(side="left", padx=18, pady=18)
        copy = tk.Frame(hero, bg="#0a0e17")
        copy.pack(side="left", fill="both", expand=True, padx=8)
        tk.Label(copy, text="AI DESK METER", bg="#0a0e17", fg="#67b7ff", font=("Helvetica", 10, "bold")).pack(anchor="w")
        self.status_label = tk.Label(copy, text=NO_ACTIVE_MUSE, bg="#0a0e17", fg="#ffd6aa", font=self.title_font)
        self.status_label.pack(anchor="w")
        self.subtitle = tk.Label(copy, text="One-command no-server GUI. Runtime writer starts automatically.", bg="#0a0e17", fg="#c8bfb6")
        self.subtitle.pack(anchor="w")

        grid = tk.Frame(self.root, bg="#05070b")
        grid.pack(fill="x", padx=24)
        self.labels: dict[str, tuple[Any, Any]] = {}
        for key, title in [("current", "Current usage"), ("weekly", "Weekly usage"), ("burn", "Burn rate"), ("provider", "Provider")]:
            frame = tk.Frame(grid, bg="#0c1019", highlightbackground="#263247", highlightthickness=1)
            frame.pack(side="left", fill="both", expand=True, padx=6, pady=6)
            tk.Label(frame, text=title, bg="#0c1019", fg="#b9afa5").pack(anchor="w", padx=12, pady=(12,2))
            value = tk.Label(frame, text="--", bg="#0c1019", fg="#fff7ed", font=self.card_font)
            value.pack(anchor="w", padx=12)
            detail = tk.Label(frame, text="waiting", bg="#0c1019", fg="#8f8781")
            detail.pack(anchor="w", padx=12, pady=(0,12))
            self.labels[key] = (value, detail)

        actions = tk.Frame(self.root, bg="#0c1019", highlightbackground="#263247", highlightthickness=1)
        actions.pack(fill="x", padx=30, pady=12)
        self.action_label = tk.Label(actions, text="Last action: no active session | In progress: none | CLI checker: inactive", bg="#0c1019", fg="#fff7ed", justify="left")
        self.action_label.pack(anchor="w", padx=14, pady=12)
        self.path_label = tk.Label(actions, text=f"Payload: {self.status_path}", bg="#0c1019", fg="#67b7ff", font=self.small_font)
        self.path_label.pack(anchor="w", padx=14, pady=(0,12))

        log_frame = tk.Frame(self.root, bg="#0c1019", highlightbackground="#263247", highlightthickness=1)
        log_frame.pack(fill="both", expand=True, padx=30, pady=(0,24))
        tk.Label(log_frame, text="Run log", bg="#0c1019", fg="#b9afa5").pack(anchor="w", padx=14, pady=(12,0))
        self.log = tk.Text(log_frame, bg="#0c1019", fg="#d9ecff", insertbackground="#fff7ed", height=10, relief="flat", font=self.small_font)
        self.log.pack(fill="both", expand=True, padx=14, pady=12)

    def draw_buddy(self) -> None:
        c = self.canvas
        c.delete("all")
        def rect(x, y, w, h, color):
            c.create_rectangle(x, y, x + w, y + h, fill=color, outline=color)
        orange = "#ff7048"; orange2 = "#ff9a5f"; blue = "#67b7ff"; cream = "#ffd6aa"; dark = "#05070b"
        c.create_rectangle(0, 0, 190, 140, fill=dark, outline=dark)
        # simple pixel buddy matching the orange/blue identity; eyes are the actual yellow pixels.
        for x in range(76, 124, 10): rect(x, 18, 8, 8, orange)
        for x in range(62, 138, 10): rect(x, 30, 8, 8, orange2 if x in (82, 112) else orange)
        for x in range(56, 144, 10): rect(x, 42, 8, 8, orange)
        for x in range(78, 124, 10): rect(x, 54, 8, 8, orange)
        rect(70, 72, 8, 8, blue); rect(82, 72, 8, 8, blue); rect(124, 72, 8, 8, blue); rect(136, 72, 8, 8, blue)
        if not self.eye_closed:
            rect(88, 40, 8, 8, cream)
            rect(114, 40, 8, 8, cream)
        label = ("✶ Musing" + "." * self.dot_count) if self.is_musing else SVG_NO_MUSE
        c.create_text(95, 118, text=label, fill=cream, font=("Helvetica", 13, "bold"))

    def _is_connected_payload(self, data: dict[str, Any]) -> bool:
        errors = data.get("errors") or []
        mode = str(data.get("mode", "")).lower()
        source = str(data.get("source") or data.get("service") or "").strip()
        status_text = str(data.get("status", "")).lower()
        return bool(source) and not errors and mode not in {"offline", "error", "planned", "disconnected", "not connected", "inactive"} and source.lower() not in {"browser-sample", "browser-preview"}

    def tick(self) -> None:
        now = time.time()
        if self.is_musing:
            self.dot_count = (self.dot_count % 3) + 1
            self.eye_closed = False
        else:
            if now >= self.next_blink:
                self.eye_closed = True
                self.blink_until = now + 0.14
                self.next_blink = now + random.uniform(3, 11)
            if self.eye_closed and now >= self.blink_until:
                self.eye_closed = False
        self.load_payload()
        self.draw_buddy()
        self.root.after(self.refresh_ms, self.tick)

    def load_payload(self) -> None:
        try:
            data = json.loads(self.status_path.read_text(encoding="utf-8"))
            connected = self._is_connected_payload(data)
            self.connected = connected
            status_text = str(data.get("status", ""))
            self.is_musing = connected and bool(data.get('muse_connected') or data.get('agent_connected') or data.get('active_muse')) and "musing" in status_text.lower()
            header = ("✶ Musing" + "." * self.dot_count) if self.is_musing else (NO_ACTIVE_MUSE if not connected else status_text or "Active")
            self.status_label.config(text=header)
            self.labels["current"][0].config(text=f"{round(_safe_number(data.get('current_percent')))}%" if connected else "--%")
            self.labels["current"][1].config(text=f"reset: {data.get('current_reset_seconds', 'unknown')}s" if connected else "reset: inactive")
            self.labels["weekly"][0].config(text=f"{round(_safe_number(data.get('weekly_percent')))}%" if connected else "--%")
            self.labels["weekly"][1].config(text=f"reset: {data.get('weekly_reset_seconds', 'unknown')}s" if connected else "reset: inactive")
            self.labels["burn"][0].config(text=str(data.get("burn_rate", "unknown")) if connected else "inactive")
            self.labels["burn"][1].config(text=f"mode: {data.get('mode', 'unknown')}" if connected else "mode: not connected")
            self.labels["provider"][0].config(text=str(data.get("source", "unknown")) if connected else "not connected")
            self.labels["provider"][1].config(text=f"updated: {data.get('updated_at', 'never')}" if connected else "updated: never")
            checker = data.get("cli_checker", {}) or {}
            self.action_label.config(text=(f"Last action: {data.get('last_action', 'unknown')} | In progress: {data.get('action_in_progress', 'musing')} | CLI checker: {checker.get('state', 'unknown')}" if connected else "Last action: no active session | In progress: none | CLI checker: inactive"))
            lines = (data.get("run_log") or ["No run log entries yet."]) if connected else ["No active Muse connected."]
            self.log.delete("1.0", "end")
            self.log.insert("end", "\n".join(map(str, lines)))
        except Exception as exc:
            self.connected = False
            self.is_musing = False
            self.status_label.config(text=NO_ACTIVE_MUSE)
            self.log.delete("1.0", "end")
            self.log.insert("end", f"No active Muse. Waiting for payload at:\n{self.status_path}\n\n{exc}")

    def close(self) -> None:
        if self.runtime_writer:
            self.runtime_writer.stop()
        self.root.destroy()


def run_gui(*, provider: str = "mock", status_path: str | Path = "runtime/status.json", interval: float = 0.5, start_runtime: bool = True) -> int:
    try:
        import tkinter as tk
    except Exception:
        # Homebrew Python on older macOS may not include _tkinter. Do not crash;
        # use the packaged Electron holster, which is the preferred cross-system app.
        from ai_meter.app_launcher import run_app

        return run_app(provider=provider, status_path=status_path, interval=interval, start_runtime=start_runtime)

    root = tk.Tk()
    TkMuseApp(root, provider=provider, status_path=Path(status_path), interval=interval, start_runtime=start_runtime)
    root.mainloop()
    return 0
