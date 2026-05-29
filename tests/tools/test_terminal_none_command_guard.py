"""终端空命令防护测试

【产品经理理解要点】
验证工具系统模块中transform sudo command none returns cleanly、terminal tool none command returns clean error的正确性
- transform sudo command none returns cleanly的正确性验证
- terminal tool none command returns clean error的正确性验证
- 影响工具系统的可靠性和功能正确性

─────────────────────────────────────────────────────────────────
Regression tests for invalid/None terminal command handling."""

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
