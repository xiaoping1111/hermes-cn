"""Regression tests for CLI prefill config key compatibility.

【产品经理理解要点】
命令行测试——验证CLI命令和交互行为中的配置管理——加载和验证YAML/ENV配置文件
"""

from __future__ import annotations

import cli


def test_resolve_prefill_messages_file_uses_top_level(monkeypatch):
    monkeypatch.delenv("HERMES_PREFILL_MESSAGES_FILE", raising=False)

    assert cli._resolve_prefill_messages_file(
        {
            "prefill_messages_file": "top.json",
            "agent": {"prefill_messages_file": "legacy.json"},
        }
    ) == "top.json"


def test_resolve_prefill_messages_file_accepts_legacy_agent_key(monkeypatch):
    monkeypatch.delenv("HERMES_PREFILL_MESSAGES_FILE", raising=False)

    assert cli._resolve_prefill_messages_file(
        {"agent": {"prefill_messages_file": "legacy.json"}}
    ) == "legacy.json"


def test_resolve_prefill_messages_file_prefers_env(monkeypatch):
    monkeypatch.setenv("HERMES_PREFILL_MESSAGES_FILE", "env.json")

    assert cli._resolve_prefill_messages_file(
        {
            "prefill_messages_file": "top.json",
            "agent": {"prefill_messages_file": "legacy.json"},
        }
    ) == "env.json"
