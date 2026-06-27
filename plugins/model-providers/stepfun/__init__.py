"""阶跃星辰 模型提供者

【产品经理理解要点】
对接阶跃星辰（StepFun）大模型服务。
- StepFun API 集成

─────────────────────────────────────────────────────────────────
StepFun provider profile."""

from providers import register_provider
from providers.base import ProviderProfile

stepfun = ProviderProfile(
    name="stepfun",
    aliases=("step", "stepfun-coding-plan"),
    default_aux_model="step-3.5-flash",
    env_vars=("STEPFUN_API_KEY",),
    base_url="https://api.stepfun.ai/step_plan/v1",
)

register_provider(stepfun)
