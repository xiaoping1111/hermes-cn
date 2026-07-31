"""Agent核心测试 - nous oauth 401 guidance

【产品经理理解要点】
Agent核心模块：Prompt构建、上下文压缩、模型路由、凭证池、记忆、LSP等中的nous oauth 401 guidance验证。
- 验证功能：nous oauth 401 guidance功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：nous oauth 401 guidance功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Tests for the Nous OAuth 401 actionable-guidance branch in
``agent.conversation_loop.run_conversation``.

Source-inspection style (matches ``test_gemini_fast_fallback.py``): we assert
that the guidance strings exist in the function body so that the user-facing
hint cannot be silently removed by a future refactor.

Regression context: ashh hit a Nous 401 (OAuth token expired / portal said
account out of credits) plus a model slug ``deepseek/deepseek-v4-flash:free``
that's OpenRouter syntax, not a Nous catalog name. The previous guidance
branch only covered ``openai-codex`` and ``xai-oauth``; ``nous`` fell through
to a generic "Your API key was rejected... run hermes setup" message, which is
the wrong advice for a pure-OAuth provider.
"""
from __future__ import annotations

import inspect

from agent import conversation_loop


def test_nous_provider_is_in_oauth_401_set():
    """The provider-set gate that selects OAuth-specific guidance must
    include ``nous`` alongside ``openai-codex`` and ``xai-oauth``.
    """
    source = inspect.getsource(conversation_loop.run_conversation)

    # Be flexible about set element ordering — assert all three are listed
    # near each other in the gating expression.
    assert "\"openai-codex\"" in source
    assert "\"xai-oauth\"" in source
    assert "\"nous\"" in source

    # And the gate string itself must mention all three so future refactors
    # that split nous off into its own gate still get caught.
    needle = "_provider in {\"openai-codex\", \"xai-oauth\", \"nous\"}"
    assert needle in source, (
        "Expected nous to be co-gated with the other OAuth providers in the "
        "actionable-401-guidance branch of run_conversation."
    )


def test_nous_401_guidance_strings_present():
    """User-facing remediation strings for Nous OAuth 401s must exist."""
    source = inspect.getsource(conversation_loop.run_conversation)

    # Must tell the user it's an OAuth token problem, NOT an API key problem
    # (Nous Portal has no API key path — auth_type=oauth_device_code only).
    assert "Nous Portal OAuth token was rejected" in source

    # Must give a concrete re-auth command, not a generic "hermes setup".
    assert "hermes portal" in source

    # Must point at the portal so users can check account/credit status.
    assert "portal.nousresearch.com" in source


