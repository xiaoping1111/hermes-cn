"""Camofox 浏览器持久化状态管理

【产品经理理解要点】
为 Camofox 浏览器提供跨重启的持久化身份，确保同一用户配置下的浏览器会话保持一致。
- 核心职责：根据 Hermes Profile 生成确定性的用户 ID 和会话 Key，Camofox 据此映射到同一浏览器配置目录
- 关键业务概念：Profile 级隔离——不同 Hermes Profile 对应不同浏览器身份，同一 Profile 重启后身份不变
- 在系统中的位置：browser_camofox.py 的依赖，提供浏览器身份参数

─────────────────────────────────────────────────────────────────
Hermes-managed Camofox state helpers.

Provides profile-scoped identity and state directory paths for Camofox
persistent browser profiles.  When managed persistence is enabled, Hermes
sends a deterministic userId derived from the active profile so that
Camofox can map it to the same persistent browser profile directory
across restarts.
"""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import Dict, Optional

from hermes_constants import get_hermes_home

CAMOFOX_STATE_DIR_NAME = "browser_auth"
CAMOFOX_STATE_SUBDIR = "camofox"


def get_camofox_state_dir() -> Path:
    """Return the profile-scoped root directory for Camofox persistence."""
    return get_hermes_home() / CAMOFOX_STATE_DIR_NAME / CAMOFOX_STATE_SUBDIR


def get_camofox_identity(task_id: Optional[str] = None) -> Dict[str, str]:
    """Return the stable Hermes-managed Camofox identity for this profile.

    The user identity is profile-scoped (same Hermes profile = same userId).
    The session key is scoped to the logical browser task so newly created
    tabs within the same profile reuse the same identity contract.
    """
    scope_root = str(get_camofox_state_dir())
    logical_scope = task_id or "default"
    user_digest = uuid.uuid5(
        uuid.NAMESPACE_URL,
        f"camofox-user:{scope_root}",
    ).hex[:10]
    session_digest = uuid.uuid5(
        uuid.NAMESPACE_URL,
        f"camofox-session:{scope_root}:{logical_scope}",
    ).hex[:16]
    return {
        "user_id": f"hermes_{user_digest}",
        "session_key": f"task_{session_digest}",
    }
