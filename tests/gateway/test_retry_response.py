"""网关retry response测试

【产品经理理解要点】
网关retry response功能测试。
- 验证功能：网关retry response处理
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：retry response功能异常

─────────────────────────────────────────────────────────────────────────
Regression test: /retry must return the agent response, not None.

Before the fix in PR #441, _handle_retry_command() called
_handle_message(retry_event) but discarded its return value with `return None`,
so users never received the final response."""
import pytest
from unittest.mock import AsyncMock, MagicMock
from gateway.run import GatewayRunner
from gateway.platforms.base import MessageEvent, MessageType


@pytest.fixture
def gateway(tmp_path):
    config = MagicMock()
    config.sessions_dir = tmp_path
    config.max_context_messages = 20
    gw = GatewayRunner.__new__(GatewayRunner)
    gw.config = config
    gw.session_store = MagicMock()
    return gw


@pytest.mark.asyncio
async def test_retry_returns_response_not_none(gateway):
    """_handle_retry_command must return the inner handler response, not None."""
    gateway.session_store.get_or_create_session.return_value = MagicMock(
        session_id="test-session"
    )
    gateway.session_store.load_transcript.return_value = [
        {"role": "user", "content": "Hello Hermes"},
        {"role": "assistant", "content": "Hi there!"},
    ]
    gateway.session_store.rewrite_transcript = MagicMock()
    expected_response = "Hi there! (retried)"
    gateway._handle_message = AsyncMock(return_value=expected_response)
    event = MessageEvent(
        text="/retry",
        message_type=MessageType.TEXT,
        source=MagicMock(),
    )
    result = await gateway._handle_retry_command(event)
    assert result is not None, "/retry must not return None"
    assert result == expected_response


