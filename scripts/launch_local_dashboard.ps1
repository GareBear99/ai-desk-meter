$ErrorActionPreference = "Stop"

$HostName = if ($env:AI_METER_HOST) { $env:AI_METER_HOST } else { "127.0.0.1" }
$Port = if ($env:AI_METER_PORT) { $env:AI_METER_PORT } else { "8787" }
$Provider = if ($env:AI_METER_PROVIDER) { $env:AI_METER_PROVIDER } else { "mock" }
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")

Write-Host "Starting AI Desk Meter local API on http://$HostName`:$Port"
Write-Host "Default provider: $Provider"

Set-Location (Join-Path $Root "host")
if (-not (Get-Command ai-meter -ErrorAction SilentlyContinue)) {
  Write-Host "ai-meter command not found; installing host package in editable mode"
  python -m pip install -e .
}

python -m ai_meter.cli serve --host $HostName --port $Port
