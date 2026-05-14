from ai_meter.providers import provider_names


def test_provider_names_include_arcrar():
    assert "arcrar" in provider_names()
    assert "mock" in provider_names()
    assert "manual" in provider_names()
