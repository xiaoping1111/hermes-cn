"""Tests for gateway /version command.

【产品经理理解要点】
网关测试——验证各平台消息收发和会话管理（test_version_command.py）
"""

import asyncio

from hermes_cli.banner import format_banner_version_label


def test_gateway_version_command_returns_release_line():
    from gateway.run import GatewayRunner

    result = asyncio.run(GatewayRunner._handle_version_command(None, None))  # type: ignore[arg-type]
    assert result == format_banner_version_label()
