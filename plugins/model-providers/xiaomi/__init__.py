"""小米MiMo模型供应商配置

【产品经理理解要点】
注册小米的MiMo系列模型供应商。
- 供应商：小米（Xiaomi），提供MiMo系列模型
- 认证：XIAOMI_API_KEY
- 注意：模型列表接口返回401，不支持健康检查
"""

from providers import register_provider
from providers.base import ProviderProfile

xiaomi = ProviderProfile(
    name="xiaomi",
    aliases=("mimo", "xiaomi-mimo"),
    env_vars=("XIAOMI_API_KEY",),
    base_url="https://api.xiaomimimo.com/v1",
    supports_health_check=False,  # /v1/models returns 401 even with valid key
)

register_provider(xiaomi)
