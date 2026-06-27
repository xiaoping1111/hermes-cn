"""HuggingFace 模型提供者

【产品经理理解要点】
对接 HuggingFace Inference API。
- HF 托管模型推理
- HF_API_KEY 认证

─────────────────────────────────────────────────────────────────
Hugging Face provider profile."""

from providers import register_provider
from providers.base import ProviderProfile

huggingface = ProviderProfile(
    name="huggingface",
    aliases=("hf", "hugging-face", "huggingface-hub"),
    env_vars=("HF_TOKEN",),
    display_name="HuggingFace",
    description="HuggingFace Inference API",
    signup_url="https://huggingface.co/settings/tokens",
    fallback_models=(
        "Qwen/Qwen3.5-72B-Instruct",
        "deepseek-ai/DeepSeek-V3.2",
    ),
    base_url="https://router.huggingface.co/v1",
)

register_provider(huggingface)
