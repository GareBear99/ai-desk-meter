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

    serve = sub.add_parser("serve", help="start local dashboard API")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8787)

    companion = sub.add_parser("companion-status", help="print compact companion-display payload as JSON")
    companion.add_argument("--provider", default="mock", choices=provider_names())

    diagnostics = sub.add_parser("diagnostics", help="write a safe diagnostics ZIP bundle")
    diagnostics.add_argument("--provider", default="mock", choices=provider_names())
    diagnostics.add_argument("--out", default="ai-desk-meter-diagnostics.zip")

    doctor = sub.add_parser("doctor", help="run a local functional health report")
    doctor.add_argument("--provider", default="mock", choices=provider_names())

    sub.add_parser("test-payload", help="print one mock payload")
    sub.add_parser("providers", help="list available providers")
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
    if args.cmd == "doctor":
        print(json.dumps(run_doctor(args.provider), indent=2))
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
