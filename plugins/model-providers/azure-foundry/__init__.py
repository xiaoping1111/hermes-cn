"""微软Azure AI Foundry模型供应商配置

【产品经理理解要点】
注册微软Azure AI Foundry供应商，提供OpenAI兼容的端点，用户需自行提供base URL。
- 供应商：Microsoft Azure AI Foundry，企业级AI模型服务
- 认证：AZURE_API_KEY，base URL按资源不同而变化，需在设置时提供
- 特点：OpenAI兼容接口，支持Azure企业认证

─────────────────────────────────────────────────────────────────
Azure Foundry exposes an OpenAI-compatible endpoint; users supply their own
base URL at setup since endpoints are per-resource.
"""

from providers import register_provider
from providers.base import ProviderProfile

azure_foundry = ProviderProfile(
    name="azure-foundry",
    aliases=("azure", "azure-ai-foundry", "azure-ai"),
    display_name="Azure Foundry",
    description="Microsoft Foundry - OpenAI-compatible endpoint (user-supplied base URL)",
    signup_url="https://ai.azure.com/",
    env_vars=("AZURE_FOUNDRY_API_KEY", "AZURE_FOUNDRY_BASE_URL"),
    base_url="",  # per-resource; user provides at setup
    auth_type="api_key",
)

register_provider(azure_foundry)
