"""电脑操作工具入口 — 让 AI 能操作鼠标键盘（macOS 专用）

【产品经理理解要点】
让 AI 能像人一样操作电脑——移动鼠标、点击、输入键盘、截图。
实际实现在 tools/computer_use/ 包中，这个文件只是注册入口。

支持两种模式：
  - 本地模式：直接操作本机（macOS 无障碍 API）
  - CUA 模式：通过 OpenAI 的 Computer Use Agent API 远程操作

─────────────────────────────────────────────────────────────────

Shim for tool discovery. Registers `computer_use` with tools.registry.

The real implementation lives in the `tools/computer_use/` package to keep
the file structure clean. This shim exists because tools.registry auto-imports
`tools/*.py` — we need a top-level module to trigger the registration.
"""

from __future__ import annotations

from tools.computer_use.schema import COMPUTER_USE_SCHEMA
from tools.computer_use.tool import (
    check_computer_use_requirements,
    handle_computer_use,
    set_approval_callback,
)
from tools.registry import registry


registry.register(
    name="computer_use",
    toolset="computer_use",
    schema=COMPUTER_USE_SCHEMA,
    handler=lambda args, **kw: handle_computer_use(args, **kw),
    check_fn=check_computer_use_requirements,
    requires_env=[],
    description=(
        "Universal macOS desktop control via cua-driver. Works with any "
        "tool-capable model (Anthropic, OpenAI, OpenRouter, local vLLM, "
        "etc.). Background computer-use: does NOT steal the user's cursor "
        "or keyboard focus."
    ),
)


__all__ = [
    "handle_computer_use",
    "set_approval_callback",
    "check_computer_use_requirements",
]
