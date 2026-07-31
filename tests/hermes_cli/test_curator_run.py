"""CLIcurator run测试

【产品经理理解要点】
CLIcurator run功能测试。
- 验证功能：命令行curator run功能
- 关键场景：配置、执行、验证
- 业务影响：curator run命令行功能失效

─────────────────────────────────────────────────────────────────────────
Tests for `hermes curator run` CLI behavior."""

from __future__ import annotations

from types import SimpleNamespace


def _args(**kwargs):
    values = {
        "dry_run": False,
        "synchronous": False,
        "background": False,
    }
    values.update(kwargs)
    return SimpleNamespace(**values)


def test_run_defaults_to_synchronous(monkeypatch, capsys):
    import agent.curator as curator_state
    import hermes_cli.curator as curator_cli

    calls = []
    monkeypatch.setattr(curator_state, "is_enabled", lambda: True)
    monkeypatch.setattr(
        curator_state,
        "run_curator_review",
        lambda **kwargs: calls.append(kwargs) or {"auto_transitions": {}},
    )

    assert curator_cli._cmd_run(_args()) == 0

    assert calls[0]["synchronous"] is True
    assert calls[0]["dry_run"] is False
    assert "background" not in capsys.readouterr().out


def test_dry_run_default_reports_synchronous_wording(monkeypatch, capsys):
    import agent.curator as curator_state
    import hermes_cli.curator as curator_cli

    monkeypatch.setattr(curator_state, "is_enabled", lambda: True)
    monkeypatch.setattr(
        curator_state,
        "run_curator_review",
        lambda **kwargs: {"auto_transitions": {}},
    )

    assert curator_cli._cmd_run(_args(dry_run=True)) == 0

    out = capsys.readouterr().out
    assert "When the report lands" not in out
    assert "Read the report with `hermes curator status`" in out
