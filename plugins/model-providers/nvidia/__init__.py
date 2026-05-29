"""NVIDIA NIM 模型供应商配置

【产品经理理解要点】
注册NVIDIA NIM加速推理平台供应商，提供NVIDIA优化的大模型推理服务。
- 供应商：NVIDIA NIM，GPU加速推理服务
- 认证：NVIDIA_API_KEY
- 备用模型：Llama-3.1-Nemotron-70B、Llama-3.3-70B等NVIDIA优化模型
- 特点：默认最大token数为16384
"""

from providers import register_provider
from providers.base import ProviderProfile

nvidia = ProviderProfile(
    name="nvidia",
    aliases=("nvidia-nim",),
    env_vars=("NVIDIA_API_KEY",),
    display_name="NVIDIA NIM",
    description="NVIDIA NIM — accelerated inference",
    signup_url="https://build.nvidia.com/",
    fallback_models=(
        "nvidia/llama-3.1-nemotron-70b-instruct",
        "nvidia/llama-3.3-70b-instruct",
    ),
    base_url="https://integrate.api.nvidia.com/v1",
    default_max_tokens=16384,
)

register_provider(nvidia)
