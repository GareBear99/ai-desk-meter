from .mock import MockProvider
from .manual import ManualProvider


def make_provider(name: str):
    if name == "mock":
        return MockProvider()
    if name == "manual":
        return ManualProvider()
    raise ValueError(f"Unknown provider: {name}")
