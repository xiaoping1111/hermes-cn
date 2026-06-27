"""Best-effort early import for the OpenAI SDK's native streaming parser.

Jiter 原生扩展预加载

【产品经理理解要点】
提前加载 OpenAI SDK 的 jiter 解析器扩展，避免 Windows 上的导入顺序失败。
- 核心职责：在 agent 包导入时预加载 jiter 原生扩展
- 关键业务概念：Windows 兼容性、导入顺序、原生扩展
- 在系统中的位置：agent/__init__.py 中的早期导入

─────────────────────────────────────────────────────────────────


The OpenAI SDK imports ``jiter`` while constructing streaming chat-completion
responses.  On some Windows installs the native extension can be imported
directly from the Hermes venv, but the first import fails when it happens later
inside the threaded streaming request path.  Loading it once during agent
package import avoids that import-order failure while preserving the normal
SDK error path for genuinely missing or broken installs.
"""

from __future__ import annotations

import importlib

_JITER_PRELOADED = False
_JITER_PRELOAD_ERROR: Exception | None = None


def preload_jiter_native_extension() -> bool:
    """Import jiter's native extension early if it is available."""

    global _JITER_PRELOADED, _JITER_PRELOAD_ERROR

    if _JITER_PRELOADED:
        return True

    try:
        importlib.import_module("jiter.jiter")
        from jiter import from_json as _from_json  # noqa: F401
    except Exception as exc:
        _JITER_PRELOAD_ERROR = exc
        return False

    _JITER_PRELOADED = True
    _JITER_PRELOAD_ERROR = None
    return True


preload_jiter_native_extension()
