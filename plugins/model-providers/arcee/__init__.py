"""【产品经理理解要点】
Arcee AI模型提供商——接入Arcee AI的模型服务，通过ARCEEAI_API_KEY认证，专注于企业级开源模型。
─────────────────────────────────────────────────────────────────
Arcee AI provider profile."""

from providers import register_provider
from providers.base import ProviderProfile

arcee = ProviderProfile(
    name="arcee",
    aliases=("arcee-ai", "arceeai"),
    env_vars=("ARCEEAI_API_KEY",),
    base_url="https://api.arcee.ai/api/v1",
)

register_provider(arcee)
