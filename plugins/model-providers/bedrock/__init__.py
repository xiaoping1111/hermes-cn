"""AWS Bedrock模型供应商配置

【产品经理理解要点】
注册AWS Bedrock供应商，通过AWS SDK认证访问Amazon Bedrock上的多厂商模型。
- 供应商：AWS Bedrock，亚马逊云上的全托管AI模型服务
- 认证：AWS SDK自动凭证链（环境变量/配置文件/角色），不走标准API Key
- 特点：无REST /v1/models端点，模型列表通过AWS SDK获取
- 支持模型：Claude、Llama、Mistral等多厂商模型
"""

from providers import register_provider
from providers.base import ProviderProfile


class BedrockProfile(ProviderProfile):
    """AWS Bedrock — no REST /v1/models endpoint; uses AWS SDK."""

    def fetch_models(
        self,
        *,
        api_key: str | None = None,
        timeout: float = 8.0,
    ) -> list[str] | None:
        """Bedrock model listing requires AWS SDK, not a REST call."""
        return None


bedrock = BedrockProfile(
    name="bedrock",
    aliases=("aws", "aws-bedrock", "amazon-bedrock", "amazon"),
    api_mode="bedrock_converse",
    env_vars=(),  # AWS SDK credentials — not env vars
    base_url="https://bedrock-runtime.us-east-1.amazonaws.com",
    auth_type="aws_sdk",
)

register_provider(bedrock)
