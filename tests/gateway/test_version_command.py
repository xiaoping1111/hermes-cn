"""网关version command测试

【产品经理理解要点】
网关version command功能测试。
- 验证功能：网关version command处理
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：version command功能异常

─────────────────────────────────────────────────────────────────────────
Tests for gateway /version command."""

import asyncio

from hermes_cli.banner import format_banner_version_label


def test_gateway_version_command_returns_release_line():
    from gateway.run import GatewayRunner

    result = asyncio.run(GatewayRunner._handle_version_command(None, None))  # type: ignore[arg-type]
    assert result == format_banner_version_label()
