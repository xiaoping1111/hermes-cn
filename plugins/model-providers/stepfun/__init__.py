"""阶跃星辰(StepFun)模型供应商配置

【产品经理理解要点】
注册阶跃星辰(StepFun)的AI模型供应商。
- 供应商：StepFun（阶跃星辰），提供Step系列模型
- 认证：STEPFUN_API_KEY
- 辅助模型：step-3.5-flash（用于压缩、视觉等辅助任务）
"""

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
