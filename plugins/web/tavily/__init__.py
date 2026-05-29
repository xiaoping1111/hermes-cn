"""Tavily网络搜索插件 — 自动加载

【产品经理理解要点】
Tavily搜索/提取/抓取插件的注册入口。首个同时支持搜索、内容提取和网站抓取的插件。
- 核心职责：将Tavily供应商注册到Hermes的搜索调度系统
- 三合一能力：搜索(web_search) + 内容提取(web_extract) + 网站抓取(web_crawl)
- 依赖：TAVILY_API_KEY环境变量

─────────────────────────────────────────────────────────────────
First plugin in this codebase to advertise ``supports_crawl=True``. The
crawl method maps to Tavily's ``/crawl`` endpoint, which accepts a seed
URL plus optional instructions and extract depth.
"""

from __future__ import annotations

from plugins.web.tavily.provider import TavilyWebSearchProvider


def register(ctx) -> None:
    """Register the Tavily provider with the plugin context."""
    ctx.register_web_search_provider(TavilyWebSearchProvider())
