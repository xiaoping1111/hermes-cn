"""Kimi / Moonshot 模型供应商配置

【产品经理理解要点】
注册月之暗面(Kimi/Moonshot)的AI模型供应商。支持双端点路由：新版sk-kimi密钥走编码专用API，旧版密钥走标准API。
- 供应商：Kimi（月之暗面），提供Moonshot系列模型
- 双端点：sk-kimi-*密钥→api.kimi.com/coding，旧版密钥→api.moonshot.ai/v1
- 认证：KIMI_API_KEY或MOONSHOT_API_KEY
- 特点：Kimi编码端点支持服务端管理温度参数（不发送temperature）

─────────────────────────────────────────────────────────────────
Kimi has dual endpoints:
  - sk-kimi-* keys → api.kimi.com/coding (Anthropic Messages API)
  - legacy keys → api.moonshot.ai/v1 (OpenAI chat completions)

This module covers the chat_completions path (/v1 endpoint).
"""

from typing import Any

from providers import register_provider
from providers.base import OMIT_TEMPERATURE, ProviderProfile


class KimiProfile(ProviderProfile):
    """Kimi/Moonshot — temperature omitted, thinking + reasoning_effort."""

    def build_api_kwargs_extras(
        self, *, reasoning_config: dict | None = None, **context
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """Kimi uses extra_body.thinking + top-level reasoning_effort."""
        extra_body = {}
        top_level = {}

        if not reasoning_config or not isinstance(reasoning_config, dict):
            # No config → thinking enabled, default effort
            extra_body["thinking"] = {"type": "enabled"}
            top_level["reasoning_effort"] = "medium"
            return extra_body, top_level

        enabled = reasoning_config.get("enabled", True)
        if enabled is False:
            extra_body["thinking"] = {"type": "disabled"}
            return extra_body, top_level

        # Enabled
        extra_body["thinking"] = {"type": "enabled"}
        effort = (reasoning_config.get("effort") or "").strip().lower()
        if effort in {"low", "medium", "high"}:
            top_level["reasoning_effort"] = effort
        else:
            top_level["reasoning_effort"] = "medium"

        return extra_body, top_level


kimi = KimiProfile(
    name="kimi-coding",
    aliases=("kimi", "moonshot", "kimi-for-coding"),
    env_vars=("KIMI_API_KEY", "KIMI_CODING_API_KEY"),
    base_url="https://api.moonshot.ai/v1",
    fixed_temperature=OMIT_TEMPERATURE,
    default_max_tokens=32000,
    default_headers={"User-Agent": "hermes-agent/1.0"},
    default_aux_model="kimi-k2-turbo-preview",
)

kimi_cn = KimiProfile(
    name="kimi-coding-cn",
    aliases=("kimi-cn", "moonshot-cn"),
    env_vars=("KIMI_CN_API_KEY",),
    base_url="https://api.moonshot.cn/v1",
    fixed_temperature=OMIT_TEMPERATURE,
    default_max_tokens=32000,
    default_headers={"User-Agent": "hermes-agent/1.0"},
    default_aux_model="kimi-k2-turbo-preview",
)

register_provider(kimi)
register_provider(kimi_cn)
