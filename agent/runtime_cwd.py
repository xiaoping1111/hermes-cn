"""Single source of truth for the agent working directory.

运行时工作目录

【产品经理理解要点】
确定智能体的工作目录(CWD)，确保系统提示、工具和上下文文件使用一致路径。
- 核心职责：解析当前会话工作目录、支持多会话网关的 per-session CWD
- 关键业务概念：TERMINAL_CWD、会话 CWD、contextvar 隔离
- 在系统中的位置：系统提示和工具执行的路径基础

─────────────────────────────────────────────────────────────────


`TERMINAL_CWD` is the runtime carrier for the configured working directory
(design #19214/#19242: `terminal.cwd` is bridged once to `TERMINAL_CWD` at
gateway/cron startup). The local-CLI backend deliberately leaves it unset and
relies on the launch dir. Reading it in one place keeps the system prompt, the
tool surfaces, and context-file discovery agreeing on where the agent lives.

Multi-session gateways can pin a logical cwd via the `_SESSION_CWD`
contextvar; CLI/cron fall through to `TERMINAL_CWD`/launch cwd.
"""

import os
from contextvars import ContextVar, Token
from pathlib import Path
from typing import Any

_UNSET: Any = object()

_SESSION_CWD: ContextVar = ContextVar("HERMES_SESSION_CWD", default=_UNSET)


def set_session_cwd(cwd: str | None) -> Token:
    """Pin the logical cwd for the current context."""
    return _SESSION_CWD.set((cwd or "").strip())


def clear_session_cwd() -> None:
    _SESSION_CWD.set("")


def _session_cwd_override() -> str:
    value = _SESSION_CWD.get()
    if value is _UNSET:
        return ""
    return str(value).strip()


def resolve_agent_cwd() -> Path:
    override = _session_cwd_override()
    if override:
        p = Path(override).expanduser()
        if p.is_dir():
            return p
    raw = os.environ.get("TERMINAL_CWD", "").strip()
    if raw:
        p = Path(raw).expanduser()
        if p.is_dir():
            return p
    return Path(os.getcwd())


def resolve_context_cwd() -> Path | None:
    # None means "no configured cwd": build_context_files_prompt then falls back
    # to the launch dir (os.getcwd()) — correct for the local CLI. The gateway
    # avoids slurping its install dir by setting TERMINAL_CWD (see system_prompt.py)
    # or, per session, the _SESSION_CWD contextvar above.
    override = _session_cwd_override()
    if override:
        return Path(override).expanduser()
    raw = os.environ.get("TERMINAL_CWD", "").strip()
    return Path(raw).expanduser() if raw else None
