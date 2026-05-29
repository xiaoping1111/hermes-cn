"""Exa搜索+提取插件 — 自动加载

【产品经理理解要点】
Exa插件的注册入口。Exa提供语义/神经搜索和内容提取，是付费的高质量搜索方案。
- 核心职责：将Exa供应商注册到Hermes的搜索调度系统
- 双能力：语义搜索 + 内容提取
- 技术特点：基于语义/神经网络的搜索，比关键词搜索更智能
- SDK懒加载：为避免冷启动开销，Exa SDK按需导入

─────────────────────────────────────────────────────────────────
Backed by the official Exa SDK (``exa-py``). Both search and extract are
sync; the dispatcher in :mod:`tools.web_tools` handles the wrap when the
caller is async.
"""

from __future__ import annotations

from plugins.web.exa.provider import ExaWebSearchProvider


def register(ctx) -> None:
    """Register the Exa provider with the plugin context."""
    ctx.register_web_search_provider(ExaWebSearchProvider())
