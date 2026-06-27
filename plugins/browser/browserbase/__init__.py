"""Browserbase 浏览器插件

【产品经理理解要点】
基于 Browserbase 的云端浏览器后端。
- 云端浏览器实例管理
- 无需本地浏览器

─────────────────────────────────────────────────────────────────
Browserbase cloud browser plugin — bundled, auto-loaded.

Mirrors the ``plugins/web/<vendor>/`` and ``plugins/image_gen/openai/``
layout: ``provider.py`` holds the provider class; ``__init__.py::register``
instantiates and registers it via the plugin context.
"""

from __future__ import annotations

from plugins.browser.browserbase.provider import BrowserbaseBrowserProvider


def register(ctx) -> None:
    """Register the Browserbase provider with the plugin context."""
    ctx.register_browser_provider(BrowserbaseBrowserProvider())
