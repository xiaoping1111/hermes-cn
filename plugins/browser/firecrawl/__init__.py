"""Firecrawl 浏览器插件

【产品经理理解要点】
基于 Firecrawl 的网页抓取和渲染后端。
- JavaScript 渲染的网页抓取
- 结构化内容提取

─────────────────────────────────────────────────────────────────
Firecrawl cloud browser plugin — bundled, auto-loaded.

Distinct from ``plugins/web/firecrawl/`` (the web search/extract/crawl
plugin); both share the FIRECRAWL_API_KEY but speak to different endpoints
(``/v2/browser`` here vs ``/v2/search`` / ``/v2/scrape`` / ``/v2/crawl``
over there).
"""

from __future__ import annotations

from plugins.browser.firecrawl.provider import FirecrawlBrowserProvider


def register(ctx) -> None:
    """Register the Firecrawl cloud-browser provider with the plugin context."""
    ctx.register_browser_provider(FirecrawlBrowserProvider())
