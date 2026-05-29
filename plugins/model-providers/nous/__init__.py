"""Nous Portal模型供应商配置

【产品经理理解要点】
注册Nous Portal供应商，Hermes自家的模型代理平台，支持产品标签和推理参数定制。
- 供应商：Nous Portal，Hermes自有的模型代理网关
- 核心特性：注入产品标签(nous_portal_tags)、支持reasoning_effort推理参数
- 与系统关系：作为Hermes生态内的统一模型入口之一
"""

from typing import Any

from agent.portal_tags import nous_portal_tags
from providers import register_provider
from providers.base import ProviderProfile


class NousProfile(ProviderProfile):
    """Nous Portal — product tags, reasoning with Nous-specific omission."""

    def build_extra_body(
        self, *, session_id: str | None = None, **context
    ) -> dict[str, Any]:
        return {"tags": nous_portal_tags()}

    def build_api_kwargs_extras(
        self,
        *,
        reasoning_config: dict | None = None,
        supports_reasoning: bool = False,
        **context,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """Nous: passes full reasoning_config, but OMITS when disabled."""
        extra_body = {}
        if supports_reasoning:
            if reasoning_config is not None:
                rc = dict(reasoning_config)
                if rc.get("enabled") is False:
                    pass  # Nous omits reasoning when disabled
                else:
                    extra_body["reasoning"] = rc
            else:
                extra_body["reasoning"] = {"enabled": True, "effort": "medium"}
        return extra_body, {}


nous = NousProfile(
    name="nous",
    aliases=("nous-portal", "nousresearch"),
    env_vars=("NOUS_API_KEY",),
    display_name="Nous Research",
    description="Nous Research — Hermes model family",
    signup_url="https://nousresearch.com/",
    fallback_models=(
        "hermes-3-405b",
        "hermes-3-70b",
    ),
    base_url="https://inference.nousresearch.com/v1",
    auth_type="oauth_device_code",
)

register_provider(nous)
