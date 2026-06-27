"""工具系统测试 - memory tool import fallback

【产品经理理解要点】
工具层（MCP/浏览器/文件/图片/搜索/终端/TTS/审批等）的安全性与功能正确性中的memory tool import fallback验证。
- 验证功能：memory tool import fallback功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：memory tool import fallback功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Regression tests for memory-tool import fallbacks.
"""

import builtins
import importlib
import sys

from tools.registry import registry


def test_memory_tool_imports_without_fcntl(monkeypatch, tmp_path):
    original_import = builtins.__import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "fcntl":
            raise ImportError("simulated missing fcntl")
        return original_import(name, globals, locals, fromlist, level)

    registry.deregister("memory")
    monkeypatch.delitem(sys.modules, "tools.memory_tool", raising=False)
    monkeypatch.setattr(builtins, "__import__", fake_import)

    memory_tool = importlib.import_module("tools.memory_tool")
    monkeypatch.setattr(memory_tool, "get_memory_dir", lambda: tmp_path)

    store = memory_tool.MemoryStore(memory_char_limit=200, user_char_limit=200)
    store.load_from_disk()
    result = store.add("memory", "fact learned during import fallback test")

    assert memory_tool.fcntl is None
    assert registry.get_entry("memory") is not None
    assert result["success"] is True
