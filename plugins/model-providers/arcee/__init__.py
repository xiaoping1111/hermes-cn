"""Arcee 模型提供者

【产品经理理解要点】
对接 Arcee 模型服务。
- Arcee API 集成

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
