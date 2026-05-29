"""Firecrawl搜索+提取插件 — 自动加载

【产品经理理解要点】
Firecrawl插件的注册入口。功能最全面的网络工具供应商，支持搜索、内容提取和网站抓取，并提供直连和托管网关双通道。
- 核心职责：将Firecrawl供应商注册到Hermes的搜索调度系统
- 三合一能力：搜索 + 内容提取 + 异步网站抓取
- 双认证通道：直连(FIRECRAWL_API_KEY)或Nous托管网关（订阅用户）
- SDK延迟加载：为避免冷启动开销，SDK按需加载

─────────────────────────────────────────────────────────────────
Largest single plugin in this PR. Captures everything the previous
inline implementation in tools/web_tools.py did:

  - Lazy import of the firecrawl SDK (~200ms cold-start cost) via a
    callable proxy that defers the actual import to first use.
  - Dual client paths: direct (FIRECRAWL_API_KEY / FIRECRAWL_API_URL)
    OR Nous-hosted tool-gateway routing for subscribers, with
    web.use_gateway as the tie-breaker.
  - Per-URL scrape loop with 60s timeout, SSRF re-check after redirect,
    website-policy gating, and format-aware content selection.
  - Robust response shape normalization across SDK / direct API /
    gateway variants (search returns differ by transport).

The plugin re-exports ``Firecrawl`` (the lazy proxy) and
``check_firecrawl_api_key`` for backward-compatibility with tests and
external code that imports those names from ``tools.web_tools``.
"""

from __future__ import annotations

from plugins.web.firecrawl.provider import FirecrawlWebSearchProvider


def register(ctx) -> None:
    """Register the Firecrawl provider with the plugin context."""
    ctx.register_web_search_provider(FirecrawlWebSearchProvider())
