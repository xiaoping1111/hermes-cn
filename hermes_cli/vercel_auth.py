"""Vercel 沙箱认证状态报告

【产品经理理解要点】
检测并报告 Vercel Sandbox 环境的认证状态，用于 `hermes status` 等诊断场景。
- 检查 OIDC Token 和 API Token Tuple 两种认证方式
- 不暴露密钥值，仅报告存在/缺失状态

─────────────────────────────────────────────────────────────────
Helpers for reporting Vercel Sandbox authentication state."""

from __future__ import annotations

import os
from dataclasses import dataclass


_TOKEN_TUPLE_VARS = ("VERCEL_TOKEN", "VERCEL_PROJECT_ID", "VERCEL_TEAM_ID")


@dataclass(frozen=True)
class VercelAuthStatus:
    ok: bool
    label: str
    detail_lines: tuple[str, ...]


def _present(name: str) -> bool:
    return bool(os.getenv(name))


def describe_vercel_auth() -> VercelAuthStatus:
    """Return Vercel auth status without exposing secret values."""

    has_oidc = _present("VERCEL_OIDC_TOKEN")
    token_states = {name: _present(name) for name in _TOKEN_TUPLE_VARS}
    present_token_vars = tuple(name for name, present in token_states.items() if present)
    missing_token_vars = tuple(name for name, present in token_states.items() if not present)

    if has_oidc:
        details = [
            "mode: OIDC",
            "active env: VERCEL_OIDC_TOKEN",
            "note: OIDC tokens are development-only; use access-token auth for deployments and long-running processes",
        ]
        if present_token_vars:
            details.append(f"also present: {', '.join(present_token_vars)}")
        return VercelAuthStatus(True, "OIDC token via VERCEL_OIDC_TOKEN", tuple(details))

    if not missing_token_vars:
        return VercelAuthStatus(
            True,
            "access token + project/team via VERCEL_TOKEN, VERCEL_PROJECT_ID, VERCEL_TEAM_ID",
            (
                "mode: access token",
                "active env: VERCEL_TOKEN, VERCEL_PROJECT_ID, VERCEL_TEAM_ID",
            ),
        )

    if present_token_vars:
        return VercelAuthStatus(
            False,
            f"partial access-token auth (missing {', '.join(missing_token_vars)})",
            (
                "mode: incomplete access token",
                f"present env: {', '.join(present_token_vars)}",
                f"missing env: {', '.join(missing_token_vars)}",
                "recommended: set VERCEL_TOKEN, VERCEL_PROJECT_ID, and VERCEL_TEAM_ID together",
            ),
        )

    return VercelAuthStatus(
        False,
        "not configured",
        (
            "recommended: set VERCEL_TOKEN, VERCEL_PROJECT_ID, and VERCEL_TEAM_ID",
            "development-only alternative: set VERCEL_OIDC_TOKEN",
        ),
    )
