"""Tests for placeholder API key detection in hermes_cli.auth.

【产品经理理解要点】
CLI模块测试——验证命令行各子模块中的认证授权——管理API密钥和OAuth流程
"""

from hermes_cli.auth import has_usable_secret


def test_has_usable_secret_rejects_documented_placeholder_key() -> None:
    """Network-exposed API server key must reject static documentation placeholders."""
    assert not has_usable_secret("your_api_key_here", min_length=8)


def test_has_usable_secret_accepts_generated_key() -> None:
    """Random-looking keys should still be accepted."""
    assert has_usable_secret("b4d59f7fe8b857d0b367ef0f5710b6a4", min_length=8)
