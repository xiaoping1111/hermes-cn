"""DuckDuckGo搜索插件 — 自动加载

【产品经理理解要点】
DuckDuckGo搜索插件的注册入口。基于社区ddgs包实现，无需API密钥即可使用。
- 核心职责：将DuckDuckGo供应商注册到Hermes的搜索调度系统
- 零配置：无需API Key，安装ddgs包即可
- 仅搜索：不支持内容提取

─────────────────────────────────────────────────────────────────
Backed by the community ``ddgs`` Python package which scrapes DDG's HTML
results page. No API key required, but the package itself must be installed
(it's an optional dep — gated via :meth:`is_available`).
"""

from __future__ import annotations

from plugins.web.ddgs.provider import DDGSWebSearchProvider


def register(ctx) -> None:
    """Register the DDGS provider with the plugin context."""
    ctx.register_web_search_provider(DDGSWebSearchProvider())
