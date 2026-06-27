"""OpenAI Codex 模型提供者

【产品经理理解要点】
对接 OpenAI Codex/ChatGPT OAuth 认证的模型服务。
- Codex OAuth 认证
- 无需 API Key

─────────────────────────────────────────────────────────────────
OpenAI Codex (Responses API) provider profile."""

from providers import register_provider
from providers.base import ProviderProfile

openai_codex = ProviderProfile(
    name="openai-codex",
    aliases=("codex", "openai_codex"),
    api_mode="codex_responses",
    env_vars=(),  # OAuth external — no API key
    base_url="https://chatgpt.com/backend-api/codex",
    auth_type="oauth_external",
)

register_provider(openai_codex)
