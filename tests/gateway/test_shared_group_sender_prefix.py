"""消息网关测试 - shared·群组管理·消息发送·前缀处理

【产品经理理解要点】
验证消息网关的群组管理消息发送前缀处理功能
- 验证的功能: 共享群组发送者前缀标注
- 核心测试场景: preprocess prefixes sender for shared non thread group session、preprocess keeps plain text for default group sessions
- 业务影响: 消息网关可能出现命令丢失或平台适配错误，影响所有平台用户

─────────────────────────────────────────────────────────────────
消息网关测试 - shared·群组消息·消息发送·前缀处理

测试多平台消息接入与命令分发中shared相关的group相关的sender相关的prefix功能
"""

import pytest

from gateway.config import GatewayConfig, Platform, PlatformConfig
from gateway.platforms.base import MessageEvent
from gateway.run import GatewayRunner
from gateway.session import SessionSource


def _make_runner(config: GatewayConfig) -> GatewayRunner:
    runner = object.__new__(GatewayRunner)
    runner.config = config
    runner.adapters = {}
    runner._model = "openai/gpt-4.1-mini"
    runner._base_url = None
    return runner


@pytest.mark.asyncio
async def test_preprocess_prefixes_sender_for_shared_non_thread_group_session():
    runner = _make_runner(
        GatewayConfig(
            platforms={
                Platform.TELEGRAM: PlatformConfig(enabled=True, token="fake"),
            },
            group_sessions_per_user=False,
        )
    )
    source = SessionSource(
        platform=Platform.TELEGRAM,
        chat_id="-1002285219667",
        chat_name="Test Group",
        chat_type="group",
        user_name="Alice",
    )
    event = MessageEvent(text="hello", source=source)

    result = await runner._prepare_inbound_message_text(
        event=event,
        source=source,
        history=[],
    )

    assert result == "[Alice] hello"


@pytest.mark.asyncio
async def test_preprocess_keeps_plain_text_for_default_group_sessions():
    runner = _make_runner(
        GatewayConfig(
            platforms={
                Platform.TELEGRAM: PlatformConfig(enabled=True, token="fake"),
            },
        )
    )
    source = SessionSource(
        platform=Platform.TELEGRAM,
        chat_id="-1002285219667",
        chat_name="Test Group",
        chat_type="group",
        user_name="Alice",
    )
    event = MessageEvent(text="hello", source=source)

    result = await runner._prepare_inbound_message_text(
        event=event,
        source=source,
        history=[],
    )

    assert result == "hello"
