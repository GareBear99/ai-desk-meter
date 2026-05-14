# Arc-RAR Fixture Set

The fixture files in `examples/` define the current AI Desk Meter compatibility surface for Arc-RAR.

## Status fixtures

- `examples/arcrar_cli_status.valid.json` — normal linked backend state.
- `examples/arcrar_cli_status.warning.json` — linked backend state with warning messages.
- `examples/arcrar_cli_status.error.json` — backend-reported error shape.

## Enrichment fixtures

- `examples/arcrar_cli_receipt_latest.valid.json`
- `examples/arcrar_cli_archive_verify.valid.json`
- `examples/arcrar_cli_session_inspect.valid.json`

## Test expectation

The provider merges these command outputs into one dashboard-safe `ai-desk-meter.v1` payload. Status is required; receipt/archive/session are optional enrichment commands.

## Compatibility notes

Arc-RAR may expose more fields than shown here. AI Desk Meter intentionally reads only the small public compatibility surface it needs for display and diagnostics.
