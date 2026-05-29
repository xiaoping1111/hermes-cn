"""【产品经理理解要点】
Kilo Code模型网关提供商——接入Kilo AI的模型网关服务，通过KILOCODE_API_KEY认证，适合代码相关任务。
─────────────────────────────────────────────────────────────────
Kilo Code provider profile."""

from providers import register_provider
from providers.base import ProviderProfile

kilocode = ProviderProfile(
    name="kilocode",
    aliases=("kilo-code", "kilo", "kilo-gateway"),
    env_vars=("KILOCODE_API_KEY",),
    base_url="https://api.kilo.ai/api/gateway",
    default_aux_model="google/gemini-3-flash-preview",
)

register_provider(kilocode)
