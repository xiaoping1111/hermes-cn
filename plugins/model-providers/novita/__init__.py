"""【产品经理理解要点】
NovitaAI模型提供商——接入NovitaAI的GPU云推理服务，提供开源模型的API调用能力。
─────────────────────────────────────────────────────────────────
NovitaAI provider profile."""

from providers import register_provider
from providers.base import ProviderProfile


novita = ProviderProfile(
    name="novita",
    aliases=("novita-ai", "novitaai"),
    display_name="NovitaAI",
    description="NovitaAI — AI-native cloud for builders and agents",
    signup_url="https://novita.ai/settings/key-management",
    env_vars=("NOVITA_API_KEY", "NOVITA_BASE_URL"),
    base_url="https://api.novita.ai/openai/v1",
    auth_type="api_key",
    default_aux_model="deepseek/deepseek-v3-0324",
    fallback_models=(
        "moonshotai/kimi-k2.5",
        "minimax/minimax-m2.7",
        "zai-org/glm-5",
        "deepseek/deepseek-v3-0324",
        "deepseek/deepseek-r1-0528",
        "qwen/qwen3-235b-a22b-fp8",
    ),
)

register_provider(novita)
