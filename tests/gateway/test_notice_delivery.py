"""消息网关测试 - notice·delivery

【产品经理理解要点】
验证消息网关相关功能的正确性
- 验证的功能: 通知消息投递机制
- 核心测试场景: deliver platform notice uses private delivery when configured、deliver platform notice falls back to public when private fails、deliver platform notice uses public delivery by default
- 业务影响: 消息网关可能出现命令丢失或平台适配错误，影响所有平台用户

─────────────────────────────────────────────────────────────────
消息网关测试 - notice·delivery

测试多平台消息接入与命令分发中notice相关的delivery功能
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from gateway.config import GatewayConfig, Platform, PlatformConfig
from gateway.platforms.base import SendResult
from gateway.run import GatewayRunner
from gateway.session import SessionSource


def _make_source() -> SessionSource:
    return SessionSource(
        platform=Platform.SLACK,
        chat_id="C123",
        chat_type="channel",
        user_id="U123",
        thread_id="111.222",
    )


def _make_runner(extra=None):
    runner = object.__new__(GatewayRunner)
    runner.config = GatewayConfig(
        platforms={
            Platform.SLACK: PlatformConfig(enabled=True, token="***", extra=extra or {})
        }
    )
    adapter = MagicMock()
    adapter.send = AsyncMock(return_value=SendResult(success=True, message_id="public-1"))
    adapter.send_private_notice = AsyncMock(return_value=SendResult(success=True, message_id="private-1"))
    runner.adapters = {Platform.SLACK: adapter}
    return runner, adapter


@pytest.mark.asyncio
async def test_deliver_platform_notice_uses_private_delivery_when_configured():
    runner, adapter = _make_runner(extra={"notice_delivery": "private"})

    await runner._deliver_platform_notice(_make_source(), "hello")

    adapter.send_private_notice.assert_awaited_once_with(
        "C123",
        "U123",
        "hello",
        metadata={"thread_id": "111.222"},
    )
    adapter.send.assert_not_awaited()


@pytest.mark.asyncio
async def test_deliver_platform_notice_falls_back_to_public_when_private_fails():
    runner, adapter = _make_runner(extra={"notice_delivery": "private"})
    adapter.send_private_notice = AsyncMock(return_value=SendResult(success=False, error="nope"))

    await runner._deliver_platform_notice(_make_source(), "hello")

    adapter.send.assert_awaited_once_with("C123", "hello", metadata={"thread_id": "111.222"})


@pytest.mark.asyncio
async def test_deliver_platform_notice_uses_public_delivery_by_default():
    runner, adapter = _make_runner()

    await runner._deliver_platform_notice(_make_source(), "hello")

    adapter.send.assert_awaited_once_with("C123", "hello", metadata={"thread_id": "111.222"})
    adapter.send_private_notice.assert_not_awaited()
