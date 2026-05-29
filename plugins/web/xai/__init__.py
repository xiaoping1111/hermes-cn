"""xAI网络搜索插件 — 自动加载

【产品经理理解要点】
xAI（Grok）网络搜索插件的注册入口。通过Grok的web_search工具实现AI驱动的网络搜索。
- 核心职责：将xAI搜索供应商注册到Hermes的搜索调度系统
- 依赖：provider.py中的XAIWebSearchProvider
- 使用场景：用户配置web.search_backend为"xai"时启用

─────────────────────────────────────────────────────────────────
Mirrors the ``plugins/web/brave_free/`` layout: ``provider.py`` holds the
provider class, ``__init__.py::register(ctx)`` registers an instance.
"""

from __future__ import annotations

from plugins.web.xai.provider import XAIWebSearchProvider


def register(ctx) -> None:
    """Register the xAI Web Search provider with the plugin context."""
    ctx.register_web_search_provider(XAIWebSearchProvider())
