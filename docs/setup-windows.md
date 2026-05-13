# Windows Setup

## Host daemon

```powershell
cd host
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
ai-meter test-payload
```

## Firmware tools

Install VS Code + PlatformIO extension, then open the `firmware` folder.
