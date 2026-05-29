"""消息网关测试 - gateway·命令处理·help

【产品经理理解要点】
验证消息网关的命令处理功能
- 验证的功能: Gateway command help rendering tests
- 核心测试场景: help sanitizes slash command mentions for telegram、commands sanitizes slash command mentions for telegram、help keeps non telegram slash command mentions unchanged
- 业务影响: 消息网关可能出现命令丢失或平台适配错误，影响所有平台用户

─────────────────────────────────────────────────────────────────
Gateway command help rendering tests.
"""

import pytest

from gateway.config import Platform
from gateway.platforms.base import MessageEvent
from gateway.session import SessionSource


def _make_event(text: str, platform: Platform) -> MessageEvent:
    return MessageEvent(
        text=text,
        source=SessionSource(
            platform=platform,
            chat_id="chat-1",
            user_id="user-1",
            user_name="tester",
            chat_type="dm",
        ),
    )


def _make_runner():
    from gateway.run import GatewayRunner

    return object.__new__(GatewayRunner)


@pytest.mark.asyncio
async def test_help_sanitizes_slash_command_mentions_for_telegram(monkeypatch):
    """Telegram help output must not expose invalid uppercase/hyphenated slashes."""
    monkeypatch.setattr(
        "agent.skill_commands.get_skill_commands",
        lambda: {
            "/Linear": {"description": "Open Linear"},
            "/Custom-Thing": {"description": "Run a custom thing"},
        },
    )

    result = await _make_runner()._handle_help_command(
        _make_event("/help", Platform.TELEGRAM)
    )

    assert "`/linear`" in result
    assert "`/custom_thing`" in result
    assert "`/Linear`" not in result
    assert "`/Custom-Thing`" not in result


@pytest.mark.asyncio
async def test_commands_sanitizes_slash_command_mentions_for_telegram(monkeypatch):
    """Paginated Telegram /commands output uses Telegram-valid slash mentions."""
    monkeypatch.setattr(
        "agent.skill_commands.get_skill_commands",
        lambda: {"/Linear": {"description": "Open Linear"}},
    )

    result = await _make_runner()._handle_commands_command(
        _make_event("/commands 999", Platform.TELEGRAM)
    )

    assert "`/linear`" in result
    assert "`/Linear`" not in result


@pytest.mark.asyncio
async def test_help_keeps_non_telegram_slash_command_mentions_unchanged(monkeypatch):
    """Only Telegram needs slash mentions rewritten to Telegram command names."""
    monkeypatch.setattr(
        "agent.skill_commands.get_skill_commands",
        lambda: {"/Linear": {"description": "Open Linear"}},
    )

    result = await _make_runner()._handle_help_command(
        _make_event("/help", Platform.DISCORD)
    )

    assert "`/Linear`" in result
