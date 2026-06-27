from __future__ import annotations
"""Agent核心测试 - jiter preload

【产品经理理解要点】
Agent核心模块：Prompt构建、上下文压缩、模型路由、凭证池、记忆、LSP等中的jiter preload验证。
- 验证功能：jiter preload功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：jiter preload功能异常或存在安全隐患"""


import importlib
import sys

from agent import jiter_preload


def test_preload_jiter_native_extension_loads_sdk_parser_dependency():
    assert jiter_preload.preload_jiter_native_extension() is True
    assert "jiter.jiter" in sys.modules


def test_preload_jiter_native_extension_is_best_effort(monkeypatch):
    monkeypatch.setattr(jiter_preload, "_JITER_PRELOADED", False)

    def _raise_missing(name: str):
        assert name == "jiter.jiter"
        raise ModuleNotFoundError(name)

    monkeypatch.setattr(importlib, "import_module", _raise_missing)

    assert jiter_preload.preload_jiter_native_extension() is False
    assert jiter_preload._JITER_PRELOADED is False
    assert isinstance(jiter_preload._JITER_PRELOAD_ERROR, ModuleNotFoundError)
