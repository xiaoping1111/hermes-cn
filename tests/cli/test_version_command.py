"""CLI终端测试 - version command

【产品经理理解要点】
命令行交互界面：斜杠命令、会话管理、压缩、编辑器、状态栏、快捷键等用户体验中的version command验证。
- 验证功能：version command功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：version command功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Tests for the /version slash command.
"""

from unittest.mock import patch

from cli import HermesCLI
from hermes_cli.commands import GATEWAY_KNOWN_COMMANDS, resolve_command


def test_version_command_is_registered():
    cmd = resolve_command("version")
    assert cmd is not None
    assert cmd.name == "version"
    assert cmd.category == "Info"
    assert resolve_command("v") is cmd


def test_version_is_gateway_known():
    assert "version" in GATEWAY_KNOWN_COMMANDS
    assert "v" in GATEWAY_KNOWN_COMMANDS


def test_process_command_version_prints_version_info():
    cli_obj = HermesCLI.__new__(HermesCLI)

    with patch("hermes_cli.main._print_version_info") as mock_print:
        assert cli_obj.process_command("/version") is True

    mock_print.assert_called_once_with(check_updates=True)
