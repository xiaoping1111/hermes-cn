"""Firecrawl云浏览器插件 — 自动加载

【产品经理理解要点】
Firecrawl云浏览器供应商插件入口，通过Firecrawl的/v2/browser端点提供远程浏览器能力。与web/firecrawl插件共用API Key但端点不同。
- 核心能力：远程云端浏览器实例
- 与web插件区别：本插件用/v2/browser端点，web插件用/search/scrape/crawl端点
- 认证：共用FIRECRAWL_API_KEY

─────────────────────────────────────────────────────────────────
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
