"""网页搜索提供者插件包

【产品经理理解要点】
网页搜索后端的插件注册中心，各子目录实现不同搜索 API 的对接。
- 每个子目录遵循 plugins/web/<name>/ 布局
- 自动加载 kind:backend 并注册到 web_search_registry

─────────────────────────────────────────────────────────────────
"""

# Bundled web search providers — plugins/web/.
#
# Each subdirectory follows the image_gen plugin layout:
#   plugins/web/<name>/{plugin.yaml, __init__.py, provider.py}
#
# They auto-load via kind: backend and register via
# ctx.register_web_search_provider() into agent.web_search_registry.
