"""Z.AI / 智谱GLM 模型供应商配置

【产品经理理解要点】
注册智谱AI(Z.AI)的GLM系列模型供应商，支持GLM-5、GLM-4等模型。
- 供应商：Z.AI（智谱AI），提供GLM系列大语言模型
- 认证：支持GLM_API_KEY/ZAI_API_KEY等多种环境变量
- 备用模型：glm-5, glm-4-9b；辅助模型：glm-4.5-flash
"""

from providers import register_provider
from providers.base import ProviderProfile

zai = ProviderProfile(
    name="zai",
    aliases=("glm", "z-ai", "z.ai", "zhipu"),
    env_vars=("GLM_API_KEY", "ZAI_API_KEY", "Z_AI_API_KEY"),
    display_name="Z.AI (GLM)",
    description="Z.AI / GLM — Zhipu AI models",
    signup_url="https://z.ai/",
    fallback_models=(
        "glm-5",
        "glm-4-9b",
    ),
    base_url="https://api.z.ai/api/paas/v4",
    default_aux_model="glm-4.5-flash",
)

register_provider(zai)
