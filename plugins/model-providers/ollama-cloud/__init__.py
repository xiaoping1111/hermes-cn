"""Ollama Cloud 模型提供者

【产品经理理解要点】
对接 Ollama Cloud 托管推理服务。
- Ollama 云端推理
- 兼容本地 Ollama API

─────────────────────────────────────────────────────────────────
Ollama Cloud provider profile."""

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
