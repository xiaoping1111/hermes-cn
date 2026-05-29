"""Browser Use云浏览器插件 — 自动加载

【产品经理理解要点】
Browser Use云浏览器供应商插件入口，提供AI驱动的浏览器自动化能力。
- 核心能力：AI驱动的浏览器自动化（点击、输入、导航等）
- 认证：BROWSER_USE_API_KEY
- 使用场景：需要AI理解页面并自动操作的场景

─────────────────────────────────────────────────────────────────
Mirrors the ``plugins/web/<vendor>/`` layout: ``provider.py`` holds the
provider class; ``__init__.py::register`` instantiates and registers it.
"""

from __future__ import annotations

from plugins.browser.browser_use.provider import BrowserUseBrowserProvider


def register(ctx) -> None:
    """Register the Browser Use provider with the plugin context."""
    ctx.register_browser_provider(BrowserUseBrowserProvider())
