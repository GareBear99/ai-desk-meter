from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time
import webbrowser
from pathlib import Path


def _repo_root() -> Path:
    # host/ai_meter/app_launcher.py -> host -> repo root
    return Path(__file__).resolve().parents[2]


def _ai_meter_executable() -> str:
    scripts = Path(sys.executable).resolve().parent
    candidate = scripts / ("ai-meter.exe" if os.name == "nt" else "ai-meter")
    if candidate.exists():
        return str(candidate)
    found = shutil.which("ai-meter")
    return found or "ai-meter"


def _start_runtime(*, root: Path, provider: str, status_path: Path, interval: float) -> subprocess.Popen[str]:
    cmd = [
        _ai_meter_executable(),
        "runtime",
        "--provider",
        provider,
        "--out",
        str(status_path),
        "--interval",
        str(max(0.1, float(interval))),
    ]
    return subprocess.Popen(
        cmd,
        cwd=str(root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def _has_npm() -> bool:
    return shutil.which("npm") is not None


def _run_npm_install(app_dir: Path) -> None:
    node_modules = app_dir / "node_modules"
    if node_modules.exists():
        return
    subprocess.run(["npm", "install"], cwd=str(app_dir), check=True)


def _open_browser_fallback(root: Path, reason: str) -> int:
    html = root / "native" / "launcher" / "app" / "index.html"
    print(f"Native holster unavailable; opened browser/static fallback. Reason: {reason}", file=sys.stderr)
    try:
        webbrowser.open(html.as_uri())
    except Exception:
        print(f"Open manually: {html}", file=sys.stderr)
    return 0


def run_app(
    *,
    provider: str = "mock",
    status_path: str | Path = "runtime/status.json",
    interval: float = 0.5,
    start_runtime: bool = True,
    install_deps: bool = True,
    browser_fallback: bool = True,
) -> int:
    """Launch the packaged native app holster.

    The default path is Electron because it is a practical cross-system holster
    for Catalina, newer macOS, Windows, Linux, and desktop SBCs. The runtime
    writer remains file/stdout based and no localhost API is required.
    """

    root = _repo_root()
    status = Path(status_path)
    if not status.is_absolute():
        status = root / status
    status.parent.mkdir(parents=True, exist_ok=True)
    app_dir = root / "native" / "launcher"

    runtime_proc: subprocess.Popen[str] | None = None
    if start_runtime:
        runtime_proc = _start_runtime(root=root, provider=provider, status_path=status, interval=interval)
        time.sleep(0.5)

    try:
        if not _has_npm():
            if not browser_fallback:
                print("npm is not available; cannot launch native app holster.", file=sys.stderr)
                return 2
            return _open_browser_fallback(root, "npm is not available")

        if install_deps:
            try:
                _run_npm_install(app_dir)
            except Exception as exc:
                if not browser_fallback:
                    print(f"npm install failed for native holster: {exc}", file=sys.stderr)
                    return 3
                return _open_browser_fallback(root, f"npm install failed: {exc}")

        env = os.environ.copy()
        env["AI_METER_PROJECT_ROOT"] = str(root)
        env["AI_METER_STATUS_PATH"] = str(status)
        env["AI_METER_PROVIDER"] = provider
        env["AI_METER_INTERVAL"] = str(max(0.1, float(interval)))
        # Runtime is already owned by this Python parent by default.
        env["AI_METER_ELECTRON_OWNS_RUNTIME"] = "0" if start_runtime else "1"

        try:
            rc = subprocess.call(["npm", "start"], cwd=str(app_dir), env=env)
        except Exception as exc:
            if browser_fallback:
                return _open_browser_fallback(root, f"native holster launch failed: {exc}")
            print(f"native holster launch failed: {exc}", file=sys.stderr)
            return 4
        if rc != 0 and browser_fallback:
            return _open_browser_fallback(root, f"native holster exited with code {rc}")
        return rc
    finally:
        if runtime_proc and runtime_proc.poll() is None:
            runtime_proc.terminate()
            try:
                runtime_proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                runtime_proc.kill()


def run_browser_preview(
    *,
    provider: str = "mock",
    status_path: str | Path = "runtime/status.json",
    interval: float = 0.5,
    start_runtime: bool = True,
) -> int:
    """Open the Vite/browser preview as a fallback/dev path."""
    root = _repo_root()
    status = Path(status_path)
    if not status.is_absolute():
        status = root / status
    runtime_proc = _start_runtime(root=root, provider=provider, status_path=status, interval=interval) if start_runtime else None
    app_dir = root / "native" / "tauri"
    try:
        if not _has_npm():
            webbrowser.open((root / "docs" / "index.html").as_uri())
            return 0
        subprocess.Popen(["npm", "run", "dev"], cwd=str(app_dir))
        time.sleep(1)
        webbrowser.open("http://127.0.0.1:1420/")
        return 0
    finally:
        # browser preview is intentionally fire-and-forget; runtime process stays
        # owned by foreground CLI only when using ai-meter runtime directly.
        if runtime_proc and runtime_proc.poll() is None:
            print("Runtime writer started for browser preview. Stop this process with Ctrl+C if needed.")
