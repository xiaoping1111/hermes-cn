"""SearXNG 搜索插件

【产品经理理解要点】
SearXNG 自建元搜索引擎后端入口。
- 对接自建 SearXNG 实例

─────────────────────────────────────────────────────────────────
SearXNG search plugin — bundled, auto-loaded.

Backed by a user-hosted SearXNG instance (URL configured via ``SEARXNG_URL``).
Search-only — pair with an extract provider (firecrawl/tavily/exa) for
``web_extract`` calls.
"""

from __future__ import annotations

from plugins.web.searxng.provider import SearXNGWebSearchProvider


def register(ctx) -> None:
    """Register the SearXNG provider with the plugin context."""
    ctx.register_web_search_provider(SearXNGWebSearchProvider())
