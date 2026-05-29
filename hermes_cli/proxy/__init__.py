"""本地 OpenAI 兼容代理 —— 复用 OAuth 凭证给外部应用

【产品经理理解要点】
在本地启动一个 OpenAI 兼容的 HTTP 代理，让外部应用（OpenViking、Open WebUI 等）
无需复制 API Key，直接复用用户已登录的供应商订阅。
- 代理监听 127.0.0.1，自动替换请求的 Authorization 头为真实上游凭证
- 凭证接近过期时自动刷新
- 首批支持 Nous Portal 和 xAI Grok

─────────────────────────────────────────────────────────────────
Local OpenAI-compatible proxy that forwards to OAuth-authenticated upstreams.

Lets external apps (OpenViking, Karakeep, Open WebUI, ...) ride the user's
already-logged-in provider subscription instead of needing a static API key
copy-pasted into each app's config.

The proxy listens on ``127.0.0.1:<port>``, accepts any bearer (the client's
``Authorization`` header is discarded), and attaches the user's real
upstream credential to the forwarded request. The credential is refreshed
automatically when it approaches expiry.

First-class adapter:
  - ``nous`` — Nous Portal (https://inference-api.nousresearch.com/v1)

Future adapters can plug in by implementing ``UpstreamAdapter``.
"""

from hermes_cli.proxy.adapters.base import UpstreamAdapter

__all__ = ["UpstreamAdapter"]
