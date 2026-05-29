"""命令行界面测试 - deprecated·cwd·warning

【产品经理理解要点】
验证命令行界面相关功能的正确性
- 验证的功能: Tests for warn_deprecated_cwd_env_vars() migration warning
- 核心测试场景: messaging cwd triggers warning、terminal cwd triggers warning when config placeholder、no warning when config has explicit cwd 等共5个场景
- 业务影响: CLI命令可能出现异常，影响用户配置和操作体验

─────────────────────────────────────────────────────────────────
Tests for warn_deprecated_cwd_env_vars() migration warning.
"""

import os
import pytest


class TestDeprecatedCwdWarning:
    """Warn when MESSAGING_CWD or TERMINAL_CWD is set in .env."""

    def test_messaging_cwd_triggers_warning(self, monkeypatch, capsys):
        monkeypatch.setenv("MESSAGING_CWD", "/some/path")
        monkeypatch.delenv("TERMINAL_CWD", raising=False)

        from hermes_cli.config import warn_deprecated_cwd_env_vars
        warn_deprecated_cwd_env_vars(config={})

        captured = capsys.readouterr()
        assert "MESSAGING_CWD" in captured.err
        assert "deprecated" in captured.err.lower()
        assert "config.yaml" in captured.err

    def test_terminal_cwd_triggers_warning_when_config_placeholder(self, monkeypatch, capsys):
        monkeypatch.setenv("TERMINAL_CWD", "/project")
        monkeypatch.delenv("MESSAGING_CWD", raising=False)

        from hermes_cli.config import warn_deprecated_cwd_env_vars
        # config has placeholder cwd → TERMINAL_CWD likely from .env
        warn_deprecated_cwd_env_vars(config={"terminal": {"cwd": "."}})

        captured = capsys.readouterr()
        assert "TERMINAL_CWD" in captured.err
        assert "deprecated" in captured.err.lower()

    def test_no_warning_when_config_has_explicit_cwd(self, monkeypatch, capsys):
        monkeypatch.setenv("TERMINAL_CWD", "/project")
        monkeypatch.delenv("MESSAGING_CWD", raising=False)

        from hermes_cli.config import warn_deprecated_cwd_env_vars
        # config has explicit cwd → TERMINAL_CWD could be from config bridge
        warn_deprecated_cwd_env_vars(config={"terminal": {"cwd": "/project"}})

        captured = capsys.readouterr()
        assert "TERMINAL_CWD" not in captured.err

    def test_no_warning_when_env_clean(self, monkeypatch, capsys):
        monkeypatch.delenv("MESSAGING_CWD", raising=False)
        monkeypatch.delenv("TERMINAL_CWD", raising=False)

        from hermes_cli.config import warn_deprecated_cwd_env_vars
        warn_deprecated_cwd_env_vars(config={})

        captured = capsys.readouterr()
        assert captured.err == ""

    def test_both_deprecated_vars_warn(self, monkeypatch, capsys):
        monkeypatch.setenv("MESSAGING_CWD", "/msg/path")
        monkeypatch.setenv("TERMINAL_CWD", "/term/path")

        from hermes_cli.config import warn_deprecated_cwd_env_vars
        warn_deprecated_cwd_env_vars(config={})

        captured = capsys.readouterr()
        assert "MESSAGING_CWD" in captured.err
        assert "TERMINAL_CWD" in captured.err
