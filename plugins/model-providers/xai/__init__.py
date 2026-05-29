"""xAI (Grok) 模型供应商配置

【产品经理理解要点】
注册xAI的Grok系列模型供应商，使用codex_responses API模式。
- 供应商：xAI，提供Grok系列模型
- 认证：XAI_API_KEY
- API模式：codex_responses（支持工具调用和代码执行）
- 别名：grok, x-ai, x.ai
"""

from providers import register_provider
from providers.base import ProviderProfile

xai = ProviderProfile(
    name="xai",
    aliases=("grok", "x-ai", "x.ai"),
    api_mode="codex_responses",
    env_vars=("XAI_API_KEY",),
    base_url="https://api.x.ai/v1",
    auth_type="api_key",
)

register_provider(xai)
