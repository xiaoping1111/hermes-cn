"""Browser Use 浏览器插件

【产品经理理解要点】
基于 browser-use 的 AI 驱动浏览器自动化后端。
- AI 自主浏览和操作网页
- 视觉理解和点击操作

─────────────────────────────────────────────────────────────────
Browser Use cloud browser plugin — bundled, auto-loaded.

Mirrors the ``plugins/web/<vendor>/`` layout: ``provider.py`` holds the
provider class; ``__init__.py::register`` instantiates and registers it.
"""

from __future__ import annotations

from plugins.browser.browser_use.provider import BrowserUseBrowserProvider


def register(ctx) -> None:
    """Register the Browser Use provider with the plugin context."""
    ctx.register_browser_provider(BrowserUseBrowserProvider())
