"""工具系统测试 - terminal none command guard

【产品经理理解要点】
工具层（MCP/浏览器/文件/图片/搜索/终端/TTS/审批等）的安全性与功能正确性中的terminal none command guard验证。
- 验证功能：terminal none command guard功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：terminal none command guard功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Regression tests for invalid/None terminal command handling.
"""

import json

from tools.terminal_tool import _transform_sudo_command, terminal_tool


def test_transform_sudo_command_none_returns_cleanly():
    transformed, sudo_stdin = _transform_sudo_command(None)

    assert transformed is None
    assert sudo_stdin is None


def test_terminal_tool_none_command_returns_clean_error():
    result = json.loads(terminal_tool(None))  # type: ignore[arg-type]

    assert result["exit_code"] == -1
    assert result["status"] == "error"
    assert "expected string" in result["error"].lower()
    assert "nonetype" in result["error"].lower()
