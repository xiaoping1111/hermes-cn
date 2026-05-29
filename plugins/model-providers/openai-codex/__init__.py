"""【产品经理理解要点】
OpenAI Codex（Responses API）提供商——接入OpenAI的Codex编程模型，使用Responses API模式，通过OAuth认证（无需API Key），擅长代码生成与编程任务。
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
