"""TUI 渲染桥接

【产品经理理解要点】
将 Agent 输出的 Markdown/Diff 内容通过 Python 侧渲染器格式化后传给 TUI 前端。
- 核心职责：调用 agent.rich_output 模块进行消息格式化和 Diff 渲染，支持流式渲染
- 关键概念：渲染器可选——若 agent.rich_output 不存在则返回 None，TUI 前端自行降级处理
- 系统定位：渲染层，Agent 原始文本 → Python 格式化 → TUI 显示

─────────────────────────────────────────────────────────────────────────
Rendering bridge — routes TUI content through Python-side renderers.

When agent.rich_output exists, its functions are used. When it doesn't,
everything returns None and the TUI falls back to its own markdown.tsx.
"""

from __future__ import annotations


def render_message(text: str, cols: int = 80) -> str | None:
    try:
        from agent.rich_output import format_response
    except ImportError:
        return None

    try:
        return format_response(text, cols=cols)
    except TypeError:
        return format_response(text)
    except Exception:
        return None


def render_diff(text: str, cols: int = 80) -> str | None:
    try:
        from agent.rich_output import render_diff as _rd
    except ImportError:
        return None

    try:
        return _rd(text, cols=cols)
    except TypeError:
        return _rd(text)
    except Exception:
        return None


def make_stream_renderer(cols: int = 80):
    try:
        from agent.rich_output import StreamingRenderer
    except ImportError:
        return None

    try:
        return StreamingRenderer(cols=cols)
    except TypeError:
        return StreamingRenderer()
    except Exception:
        return None
