"""xAI Grok 模型提供者

【产品经理理解要点】
对接 xAI Grok 系列模型。
- Grok 系列模型接入
- xAI OAuth 或 API Key 认证

─────────────────────────────────────────────────────────────────
xAI (Grok) provider profile."""

from hermes_cli import __version__ as _HERMES_VERSION
from providers import register_provider
from providers.base import ProviderProfile

xai = ProviderProfile(
    name="xai",
    aliases=("grok", "x-ai", "x.ai"),
    api_mode="codex_responses",
    env_vars=("XAI_API_KEY",),
    base_url="https://api.x.ai/v1",
    auth_type="api_key",
    default_headers={"User-Agent": f"Hermes-Agent/{_HERMES_VERSION}"},
)

register_provider(xai)
