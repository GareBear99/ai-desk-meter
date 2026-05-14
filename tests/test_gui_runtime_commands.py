from __future__ import annotations

from ai_meter.cli import main


def test_gui_and_runtime_commands_registered_in_help(capsys):
    try:
        main(["-h"])
    except SystemExit:
        pass
    help_text = capsys.readouterr().out
    assert "gui" in help_text
    assert "runtime" in help_text


def test_gui_module_imports():
    from ai_meter.gui import NO_ACTIVE_MUSE, SVG_NO_MUSE

    assert NO_ACTIVE_MUSE == "No active Muse"
    assert SVG_NO_MUSE == "No Muse."
