"""CLIxai provider labels测试

【产品经理理解要点】
CLIxai provider labels功能测试。
- 验证功能：命令行xai provider labels功能
- 关键场景：配置、执行、验证
- 业务影响：xai provider labels命令行功能失效

─────────────────────────────────────────────────────────────────────────
Regression tests for xAI provider label disambiguation."""

from hermes_cli.models import provider_label
from hermes_cli.providers import get_label


def test_xai_oauth_provider_label_is_not_collapsed_to_api_key_label():
    """The model picker must distinguish xAI API-key and OAuth providers."""
    assert get_label("xai") == "xAI"
    assert get_label("xai-oauth") == "xAI Grok OAuth (SuperGrok / Premium+)"
    assert get_label("grok-oauth") == "xAI Grok OAuth (SuperGrok / Premium+)"


