"""Browserbase云浏览器插件 — 自动加载

【产品经理理解要点】
Browserbase云浏览器供应商插件入口，提供可扩展的远程浏览器实例服务。
- 核心能力：创建/管理远程浏览器实例
- 认证：BROWSERBASE_API_KEY
- 使用场景：需要大量并发的浏览器自动化场景

─────────────────────────────────────────────────────────────────
Mirrors the ``plugins/web/<vendor>/`` and ``plugins/image_gen/openai/``
layout: ``provider.py`` holds the provider class; ``__init__.py::register``
instantiates and registers it via the plugin context.
"""

from __future__ import annotations

from plugins.browser.browserbase.provider import BrowserbaseBrowserProvider


def register(ctx) -> None:
    """Register the Browserbase provider with the plugin context."""
    ctx.register_browser_provider(BrowserbaseBrowserProvider())
