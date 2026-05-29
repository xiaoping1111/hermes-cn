"""Hugging Face模型供应商配置

【产品经理理解要点】
注册HuggingFace Inference API供应商，提供开源模型推理服务。
- 供应商：HuggingFace，全球最大的开源模型社区
- 认证：HF_TOKEN
- 备用模型：Qwen3.5-72B、DeepSeek-V3.2等开源模型
- 特点：可访问数千个开源模型
"""

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
