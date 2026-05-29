"""Ollama Cloud模型供应商配置

【产品经理理解要点】
注册Ollama云端推理服务供应商，无需本地GPU即可使用Ollama模型。
- 供应商：Ollama Cloud，提供云端Ollama模型推理
- 认证：OLLAMA_API_KEY
- 辅助模型：nemotron-3-nano:30b
"""

from providers import register_provider
from providers.base import ProviderProfile

ollama_cloud = ProviderProfile(
    name="ollama-cloud",
    aliases=("ollama_cloud",),
    default_aux_model="nemotron-3-nano:30b",
    env_vars=("OLLAMA_API_KEY",),
    base_url="https://ollama.com/v1",
)

register_provider(ollama_cloud)
