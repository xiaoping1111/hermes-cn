"""阿里云通义千问模型提供者

【产品经理理解要点】
对接阿里云通义千问大模型系列。
- Qwen 系列模型接入
- 阿里云 API Key 认证

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
