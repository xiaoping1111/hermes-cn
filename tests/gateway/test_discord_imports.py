"""消息网关测试 - Discord平台·导入

【产品经理理解要点】
验证消息网关的Discord平台导入功能
- 验证的功能: Import-safety tests for the Discord gateway adapter
- 核心测试场景: module imports even when discord dependency is missing
- 业务影响: 消息网关可能出现命令丢失或平台适配错误，影响所有平台用户

─────────────────────────────────────────────────────────────────
Import-safety tests for the Discord gateway adapter.
"""

import builtins
import importlib
import sys


class TestDiscordImportSafety:
    def test_module_imports_even_when_discord_dependency_is_missing(self, monkeypatch):
        original_import = builtins.__import__

        def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "discord" or name.startswith("discord."):
                raise ImportError("discord unavailable for test")
            return original_import(name, globals, locals, fromlist, level)

        monkeypatch.delitem(sys.modules, "gateway.platforms.discord", raising=False)
        monkeypatch.setattr(builtins, "__import__", fake_import)

        module = importlib.import_module("gateway.platforms.discord")

        assert module.DISCORD_AVAILABLE is False
        assert module.discord is None
