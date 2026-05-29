"""【产品经理理解要点】
阿里云DashScope模型提供商——接入阿里云百炼/DashScope平台的模型服务（通义千问等），通过DASHSCOPE_API_KEY认证，使用国际版端点。
─────────────────────────────────────────────────────────────────
Alibaba Cloud DashScope provider profile."""

from providers import register_provider
from providers.base import ProviderProfile

alibaba = ProviderProfile(
    name="alibaba",
    aliases=("dashscope", "alibaba-cloud", "qwen-dashscope"),
    env_vars=("DASHSCOPE_API_KEY",),
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
)

register_provider(alibaba)
