"""CLI终端测试 - prefill config

【产品经理理解要点】
命令行交互界面：斜杠命令、会话管理、压缩、编辑器、状态栏、快捷键等用户体验中的prefill config验证。
- 验证功能：prefill config功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：prefill config功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Regression tests for CLI prefill config key compatibility.
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
