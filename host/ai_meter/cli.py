from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from ai_meter import __version__
from ai_meter.companion import to_companion_payload
from ai_meter.doctor import run_doctor
from ai_meter.config import load_config
from ai_meter.diagnostics import write_diagnostics_zip
from ai_meter.providers import make_provider, provider_names
from ai_meter.transports import make_transport
from ai_meter.writer import read_provider_payload, watch_writer, write_companion, write_status


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="ai-meter", description="AI Desk Meter host daemon")
    sub = p.add_subparsers(dest="cmd", required=True)

    start = sub.add_parser("start", help="start host loop")
    start.add_argument("--config", default=None)
    start.add_argument("--provider", default=None, choices=provider_names())
    start.add_argument("--transport", default=None, choices=["stdout", "wifi"])
    start.add_argument("--url", default=None)
    start.add_argument("--poll", type=int, default=None)
    start.add_argument("--once", action="store_true")

    status = sub.add_parser("status", help="print one provider payload as formatted JSON")
    status.add_argument("--provider", default="mock", choices=provider_names())

    serve = sub.add_parser("serve", help="start optional local dashboard API for development/debug previews")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8787)

    gui = sub.add_parser("gui", help="open the no-server GUI and automatically start the runtime writer")
    gui.add_argument("--provider", default="mock", choices=provider_names())
    gui.add_argument("--out", default="runtime/status.json", help="status JSON path used by the GUI")
    gui.add_argument("--interval", type=float, default=0.5)
    gui.add_argument("--no-runtime", action="store_true", help="open GUI without starting the background writer")

    app = sub.add_parser("app", help="open the packaged native app holster and automatically start runtime")
    app.add_argument("--provider", default="mock", choices=provider_names())
    app.add_argument("--out", default="runtime/status.json", help="status JSON path used by the native app")
    app.add_argument("--interval", type=float, default=0.5)
    app.add_argument("--no-runtime", action="store_true", help="open native app without starting the background writer")
    app.add_argument("--no-install", action="store_true", help="do not run npm install automatically for the native launcher")

    runtime = sub.add_parser("runtime", help="run the no-GUI runtime writer until stopped")
    runtime.add_argument("--provider", default="mock", choices=provider_names())
    runtime.add_argument("--out", default="runtime/status.json")
    runtime.add_argument("--interval", type=float, default=0.5)

    companion = sub.add_parser("companion-status", help="print compact companion-display payload as JSON")
    companion.add_argument("--provider", default="mock", choices=provider_names())


    write_status_p = sub.add_parser("write-status", help="write one full provider payload to a JSON file; no local server required")
    write_status_p.add_argument("--provider", default="mock", choices=provider_names())
    write_status_p.add_argument("--out", default="runtime/status.json")

    write_companion_p = sub.add_parser("write-companion", help="write one compact companion payload to a JSON file; no local server required")
    write_companion_p.add_argument("--provider", default="mock", choices=provider_names())
    write_companion_p.add_argument("--out", default="runtime/companion.json")

    watch = sub.add_parser("watch", help="continuously write full provider payload JSON; no local server required")
    watch.add_argument("--provider", default="mock", choices=provider_names())
    watch.add_argument("--out", default="runtime/status.json")
    watch.add_argument("--interval", type=float, default=0.5)
    watch.add_argument("--count", type=int, default=None, help=argparse.SUPPRESS)

    watch_companion = sub.add_parser("watch-companion", help="continuously write compact companion JSON; no local server required")
    watch_companion.add_argument("--provider", default="mock", choices=provider_names())
    watch_companion.add_argument("--out", default="runtime/companion.json")
    watch_companion.add_argument("--interval", type=float, default=0.5)
    watch_companion.add_argument("--count", type=int, default=None, help=argparse.SUPPRESS)

    diagnostics = sub.add_parser("diagnostics", help="write a safe diagnostics ZIP bundle")
    diagnostics.add_argument("--provider", default="mock", choices=provider_names())
    diagnostics.add_argument("--out", default="ai-desk-meter-diagnostics.zip")

    doctor = sub.add_parser("doctor", help="run a local functional health report")
    doctor.add_argument("--provider", default="mock", choices=provider_names())

    sub.add_parser("test-payload", help="print one mock payload")
    sub.add_parser("providers", help="list available providers")
    check_cli = sub.add_parser("check-cli", help="print CLI checker state as JSON")
    check_cli.add_argument("--provider", default="mock", choices=provider_names())

    sub.add_parser("version", help="print the installed ai-desk-meter version")
    return p


def cmd_start(args: argparse.Namespace) -> int:
    cfg = load_config(args.config)
    provider_name = args.provider or cfg.provider
    transport_name = args.transport or cfg.transport
    poll = args.poll or cfg.poll_seconds
    url = args.url or cfg.url

    provider = make_provider(provider_name)
    transport = make_transport(transport_name, url)

    while True:
        try:
            payload = provider.read()
            transport.send(payload)
        except KeyboardInterrupt:
            return 0
        except Exception as exc:
            print(f"ai-meter error: {exc}", file=sys.stderr)
        if args.once:
            return 0
        time.sleep(max(1, poll))


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.cmd == "status":
        payload = make_provider(args.provider).read()
        print(json.dumps(payload.to_wire(), indent=2))
        return 0
    if args.cmd == "companion-status":
        payload = make_provider(args.provider).read()
        print(json.dumps(to_companion_payload(payload), indent=2))
        return 0
    if args.cmd == "test-payload":
        payload = make_provider("mock").read()
        print(json.dumps(payload.to_wire(), indent=2))
        return 0
    if args.cmd == "providers":
        print("\n".join(provider_names()))
        return 0
    if args.cmd == "version":
        print(__version__)
        return 0
    if args.cmd == "check-cli":
        payload = read_provider_payload(args.provider, action="CLI checker probe complete")
        print(json.dumps({
            "schema": "ai-desk-meter.cli-checker.v1",
            "ok": not bool(payload.errors),
            "provider": args.provider,
            "last_action": payload.last_action,
            "action_in_progress": payload.action_in_progress,
            "cli_checker": payload.cli_checker,
            "warnings": payload.warnings,
            "errors": payload.errors,
        }, indent=2))
        return 0
    if args.cmd == "doctor":
        print(json.dumps(run_doctor(args.provider), indent=2))
        return 0
    if args.cmd == "gui":
        from ai_meter.gui import run_gui

        return run_gui(provider=args.provider, status_path=args.out, interval=args.interval, start_runtime=not args.no_runtime)
    if args.cmd == "app":
        from ai_meter.app_launcher import run_app

        return run_app(provider=args.provider, status_path=args.out, interval=args.interval, start_runtime=not args.no_runtime, install_deps=not args.no_install)
    if args.cmd == "runtime":
        try:
            watch_writer(
                path=Path(args.out),
                provider_name=args.provider,
                interval_seconds=args.interval,
                companion=False,
                count=None,
                on_write=lambda p: print(str(p), flush=True),
            )
            return 0
        except KeyboardInterrupt:
            return 0

    if args.cmd == "write-status":
        out = write_status(Path(args.out), args.provider)
        print(str(out))
        return 0
    if args.cmd == "write-companion":
        out = write_companion(Path(args.out), args.provider)
        print(str(out))
        return 0
    if args.cmd == "watch":
        try:
            watch_writer(
                path=Path(args.out),
                provider_name=args.provider,
                interval_seconds=args.interval,
                companion=False,
                count=args.count,
                on_write=lambda p: print(str(p), flush=True),
            )
            return 0
        except KeyboardInterrupt:
            return 0
    if args.cmd == "watch-companion":
        try:
            watch_writer(
                path=Path(args.out),
                provider_name=args.provider,
                interval_seconds=args.interval,
                companion=True,
                count=args.count,
                on_write=lambda p: print(str(p), flush=True),
            )
            return 0
        except KeyboardInterrupt:
            return 0
    if args.cmd == "diagnostics":
        out = write_diagnostics_zip(Path(args.out), args.provider)
        print(str(out))
        return 0
    if args.cmd == "serve":
        from ai_meter.server import run_server

        run_server(args.host, args.port)
        return 0
    if args.cmd == "start":
        return cmd_start(args)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
