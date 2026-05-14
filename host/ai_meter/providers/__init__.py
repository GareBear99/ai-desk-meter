from .arcrar import ArcRarProvider
from .arcrar_cli import ArcRarCliProvider
from .manual import ManualProvider
from .mock import MockProvider


PROVIDERS = {
    "arcrar": ArcRarProvider,
    "arcrar-cli": ArcRarCliProvider,
    "manual": ManualProvider,
    "mock": MockProvider,
}


def make_provider(name: str):
    try:
        return PROVIDERS[name]()
    except KeyError as exc:
        available = ", ".join(sorted(PROVIDERS))
        raise ValueError(f"Unknown provider: {name}. Available providers: {available}") from exc


def provider_names() -> list[str]:
    return sorted(PROVIDERS)
