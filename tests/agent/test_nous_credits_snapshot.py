"""Agent核心测试 - nous credits snapshot

【产品经理理解要点】
Agent核心模块：Prompt构建、上下文压缩、模型路由、凭证池、记忆、LSP等中的nous credits snapshot验证。
- 验证功能：nous credits snapshot功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：nous credits snapshot功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Tests for build_nous_credits_snapshot (L6-A, magnitudes-only).
"""

from __future__ import annotations

from agent.account_usage import build_nous_credits_snapshot
from hermes_cli.nous_account import (
    NousPaidServiceAccessInfo,
    NousPortalAccountInfo,
    NousPortalSubscriptionInfo,
)


def _account(**kwargs) -> NousPortalAccountInfo:
    kwargs.setdefault("logged_in", True)
    kwargs.setdefault("source", "account_api")
    kwargs.setdefault("fresh", True)
    return NousPortalAccountInfo(**kwargs)


def _all_lines(snapshot) -> list[str]:
    return list(snapshot.details)


def test_healthy():
    info = _account(
        paid_service_access=True,
        paid_service_access_info=NousPaidServiceAccessInfo(
            subscription_credits_remaining=18.0,
            purchased_credits_remaining=12.34,
            total_usable_credits=30.34,
        ),
        subscription=NousPortalSubscriptionInfo(
            plan="Pro",
            current_period_end="2026-07-01",
        ),
    )
    snap = build_nous_credits_snapshot(info)
    assert snap is not None
    assert snap.available is True
    assert snap.plan == "Pro"
    assert snap.provider == "nous"
    assert snap.title == "Nous credits"
    blob = "\n".join(_all_lines(snap))
    assert "$18.00" in blob
    assert "$12.34" in blob
    assert "$30.34" in blob
    assert "Renews: 2026-07-01" in blob
    assert "/billing" in blob
    # money-rule: magnitudes-only, never a percentage
    assert "%" not in blob








def test_logged_out():
    info = _account(
        logged_in=False,
        paid_service_access=True,
        paid_service_access_info=NousPaidServiceAccessInfo(
            total_usable_credits=10.0,
        ),
    )
    assert build_nous_credits_snapshot(info) is None


def test_none():
    assert build_nous_credits_snapshot(None) is None






