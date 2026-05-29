"""消息网关测试 - Matrix平台·exec·approval

【产品经理理解要点】
验证消息网关的Matrix平台功能
- 验证的功能: Matrix平台Codex执行审批流程
- 核心测试场景: send exec approval registers prompt and seeds reactions、reaction resolves pending approval
- 业务影响: 消息网关可能出现命令丢失或平台适配错误，影响所有平台用户

─────────────────────────────────────────────────────────────────
消息网关测试 - Matrix平台适配·Codex执行路径·approval

测试多平台消息接入与命令分发中matrix相关的exec相关的approval功能
"""

import types

import pytest
from unittest.mock import AsyncMock, patch

from gateway.config import PlatformConfig


class TestMatrixExecApprovalReactions:
    @pytest.mark.asyncio
    async def test_send_exec_approval_registers_prompt_and_seeds_reactions(self, monkeypatch):
        monkeypatch.setenv("MATRIX_ALLOWED_USERS", "@liizfq:liizfq.top")
        from gateway.platforms.matrix import MatrixAdapter

        adapter = MatrixAdapter(PlatformConfig(enabled=True, token="tok", extra={"homeserver": "https://matrix.example.org"}))
        adapter._client = types.SimpleNamespace()
        adapter.send = AsyncMock(return_value=types.SimpleNamespace(success=True, message_id="$evt1"))
        adapter._send_reaction = AsyncMock(return_value="$r")

        result = await adapter.send_exec_approval(
            chat_id="!room:example.org",
            command="rm -rf /tmp/test",
            session_key="sess-1",
            description="dangerous",
        )

        assert result.success is True
        assert adapter._approval_prompt_by_session["sess-1"] == "$evt1"
        assert adapter._approval_prompts_by_event["$evt1"].session_key == "sess-1"
        assert adapter._send_reaction.await_count == 2
        emojis = [call.args[2] for call in adapter._send_reaction.await_args_list]
        assert emojis == ["✅", "❎"]

    @pytest.mark.asyncio
    async def test_reaction_resolves_pending_approval(self, monkeypatch):
        monkeypatch.setenv("MATRIX_ALLOWED_USERS", "@liizfq:liizfq.top")
        from gateway.platforms.matrix import MatrixAdapter, _MatrixApprovalPrompt

        adapter = MatrixAdapter(PlatformConfig(enabled=True, token="tok", extra={"homeserver": "https://matrix.example.org"}))
        # Resolve user_id so _is_self_sender doesn't defensively drop all traffic (#15763).
        adapter._user_id = "@bot:example.org"
        adapter._approval_prompts_by_event["$target"] = _MatrixApprovalPrompt(
            session_key="sess-1", chat_id="!room:example.org", message_id="$target"
        )
        adapter._approval_prompt_by_session["sess-1"] = "$target"

        content = {"m.relates_to": {"event_id": "$target", "key": "✅"}}
        event = types.SimpleNamespace(
            sender="@liizfq:liizfq.top",
            event_id="$react1",
            room_id="!room:example.org",
            content=content,
        )

        with patch("tools.approval.resolve_gateway_approval", return_value=1) as mock_resolve:
            await adapter._on_reaction(event)

        mock_resolve.assert_called_once_with("sess-1", "once")
        assert "$target" not in adapter._approval_prompts_by_event
        assert "sess-1" not in adapter._approval_prompt_by_session
