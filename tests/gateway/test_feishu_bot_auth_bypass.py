"""消息网关测试 - feishu·机器人过滤·认证授权·bypass

【产品经理理解要点】
验证消息网关的机器人过滤认证授权功能
- 验证的功能: Regression guard for Feishu bot-sender authorization bypass
- 核心测试场景: feishu bot authorized when allow bots mentions、feishu bot authorized when allow bots all、feishu bot NOT authorized when allow bots none 等共6个场景
- 业务影响: 消息网关可能出现命令丢失或平台适配错误，影响所有平台用户

─────────────────────────────────────────────────────────────────
Regression guard for Feishu bot-sender authorization bypass.

Mirrors tests/gateway/test_discord_bot_auth_bypass.py for Platform.FEISHU.
Without the bypass in gateway/run.py, Feishu bot senders admitted by the
adapter would be rejected at _is_user_authorized with "Unauthorized user"
— same class of bug as Discord #4466.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from gateway.session import Platform, SessionSource


@pytest.fixture(autouse=True)
def _isolate_feishu_env(monkeypatch):
    for var in (
        "FEISHU_ALLOW_BOTS",
        "FEISHU_ALLOWED_USERS",
        "FEISHU_ALLOW_ALL_USERS",
        "GATEWAY_ALLOW_ALL_USERS",
        "GATEWAY_ALLOWED_USERS",
    ):
        monkeypatch.delenv(var, raising=False)


def _make_bare_runner():
    from gateway.run import GatewayRunner

    runner = object.__new__(GatewayRunner)
    runner.pairing_store = SimpleNamespace(is_approved=lambda *_a, **_kw: False)
    return runner


def _make_feishu_bot_source(open_id: str = "ou_peer"):
    return SessionSource(
        platform=Platform.FEISHU,
        chat_id="oc_1",
        chat_type="group",
        user_id=open_id,
        user_name="PeerBot",
        is_bot=True,
    )


def _make_feishu_human_source(open_id: str = "ou_human"):
    return SessionSource(
        platform=Platform.FEISHU,
        chat_id="oc_1",
        chat_type="group",
        user_id=open_id,
        user_name="Human",
        is_bot=False,
    )


def test_feishu_bot_authorized_when_allow_bots_mentions(monkeypatch):
    runner = _make_bare_runner()
    monkeypatch.setenv("FEISHU_ALLOW_BOTS", "mentions")
    monkeypatch.setenv("FEISHU_ALLOWED_USERS", "ou_human")

    assert runner._is_user_authorized(_make_feishu_bot_source("ou_peer")) is True


def test_feishu_bot_authorized_when_allow_bots_all(monkeypatch):
    runner = _make_bare_runner()
    monkeypatch.setenv("FEISHU_ALLOW_BOTS", "all")
    monkeypatch.setenv("FEISHU_ALLOWED_USERS", "ou_human")

    assert runner._is_user_authorized(_make_feishu_bot_source()) is True


def test_feishu_bot_NOT_authorized_when_allow_bots_none(monkeypatch):
    runner = _make_bare_runner()
    monkeypatch.setenv("FEISHU_ALLOW_BOTS", "none")
    monkeypatch.setenv("FEISHU_ALLOWED_USERS", "ou_human")

    assert runner._is_user_authorized(_make_feishu_bot_source("ou_peer")) is False


def test_feishu_bot_NOT_authorized_when_allow_bots_unset(monkeypatch):
    runner = _make_bare_runner()
    monkeypatch.setenv("FEISHU_ALLOWED_USERS", "ou_human")

    assert runner._is_user_authorized(_make_feishu_bot_source("ou_peer")) is False


def test_feishu_human_still_checked_against_allowlist_when_bot_policy_set(monkeypatch):
    """FEISHU_ALLOW_BOTS=all must NOT open the gate for humans."""
    runner = _make_bare_runner()
    monkeypatch.setenv("FEISHU_ALLOW_BOTS", "all")
    monkeypatch.setenv("FEISHU_ALLOWED_USERS", "ou_human")

    assert runner._is_user_authorized(_make_feishu_human_source("ou_stranger")) is False
    assert runner._is_user_authorized(_make_feishu_human_source("ou_human")) is True


def test_feishu_bot_bypass_does_not_leak_to_other_platforms(monkeypatch):
    """FEISHU_ALLOW_BOTS=all must not authorize Telegram/Discord bot sources."""
    runner = _make_bare_runner()
    monkeypatch.setenv("FEISHU_ALLOW_BOTS", "all")

    telegram_bot = SessionSource(
        platform=Platform.TELEGRAM,
        chat_id="123",
        chat_type="channel",
        user_id="999",
        is_bot=True,
    )
    assert runner._is_user_authorized(telegram_bot) is False
