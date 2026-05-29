"""SearXNG搜索插件 — 自动加载

【产品经理理解要点】
SearXNG自托管元搜索插件的注册入口。用户需自行部署SearXNG实例，免费且隐私友好。
- 核心职责：将SearXNG供应商注册到Hermes的搜索调度系统
- 仅支持搜索：不支持内容提取，需搭配其他提取供应商（如Firecrawl/Tavily/Exa）
- 部署要求：需要自建SearXNG实例并配置SEARXNG_URL环境变量

─────────────────────────────────────────────────────────────────
Backed by a user-hosted SearXNG instance (URL configured via ``SEARXNG_URL``).
Search-only — pair with an extract provider (firecrawl/tavily/exa) for
``web_extract`` calls.
"""

from __future__ import annotations

from plugins.web.searxng.provider import SearXNGWebSearchProvider


def register(ctx) -> None:
    """Register the SearXNG provider with the plugin context."""
    ctx.register_web_search_provider(SearXNGWebSearchProvider())
