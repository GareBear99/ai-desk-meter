from .stdout import StdoutTransport
from .wifi import WifiTransport


def make_transport(name: str, url: str | None = None):
    if name == "stdout":
        return StdoutTransport()
    if name == "wifi":
        return WifiTransport(url or "http://127.0.0.1/api/state")
    raise ValueError(f"Unknown transport: {name}")
