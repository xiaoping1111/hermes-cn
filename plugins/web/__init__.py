"""网络搜索供应商插件集合

【产品经理理解要点】
Hermes所有网络搜索能力的插件入口。每个子目录代表一个搜索供应商（如Brave、Tavily、Exa等），由插件系统自动加载注册。
- 核心职责：统一管理多种网络搜索/网页提取/网站抓取服务
- 支持能力：搜索(web_search)、内容提取(web_extract)、网站抓取(web_crawl)
- 供应商示例：Brave(免费搜索)、Tavily(搜索+提取+抓取)、Firecrawl(搜索+提取+抓取)
"""

# Bundled web search providers — plugins/web/.
#
# Each subdirectory follows the image_gen plugin layout:
#   plugins/web/<name>/{plugin.yaml, __init__.py, provider.py}
#
# They auto-load via kind: backend and register via
# ctx.register_web_search_provider() into agent.web_search_registry.
