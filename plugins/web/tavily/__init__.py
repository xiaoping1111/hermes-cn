"""Tavily 搜索插件

【产品经理理解要点】
Tavily AI 搜索后端入口。
- 专为 AI Agent 优化的搜索 API

─────────────────────────────────────────────────────────────────
Tavily web search + extract plugin — bundled, auto-loaded."""

from __future__ import annotations

from plugins.web.tavily.provider import TavilyWebSearchProvider


def register(ctx) -> None:
    """Register the Tavily provider with the plugin context."""
    ctx.register_web_search_provider(TavilyWebSearchProvider())
