"""工具系统测试 - image generation env

【产品经理理解要点】
工具层（MCP/浏览器/文件/图片/搜索/终端/TTS/审批等）的安全性与功能正确性中的image generation env验证。
- 验证功能：image generation env功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：image generation env功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
FAL_KEY env var normalization (whitespace-only treated as unset).
"""


def test_fal_key_whitespace_is_unset(monkeypatch):
    # Whitespace-only FAL_KEY must NOT register as configured, and the managed
    # gateway fallback must be disabled for this assertion to be meaningful.
    monkeypatch.setenv("FAL_KEY", "   ")

    from tools import image_generation_tool

    monkeypatch.setattr(
        image_generation_tool, "_resolve_managed_fal_gateway", lambda: None
    )

    assert image_generation_tool.check_fal_api_key() is False


# ---------------------------------------------------------------------------
# Actionable setup message when no FAL backend is reachable.
# Regression for the silent-drop UX gap described in issue #2543.
# ---------------------------------------------------------------------------


def test_image_generate_tool_returns_actionable_error_when_no_backend(monkeypatch):
    """End-to-end: handler must surface the actionable message, not a bare string."""
    import json

    from tools import image_generation_tool

    monkeypatch.setattr(
        image_generation_tool, "fal_key_is_configured", lambda: False
    )
    monkeypatch.setattr(
        image_generation_tool, "_resolve_managed_fal_gateway", lambda: None
    )
    monkeypatch.setattr(
        image_generation_tool, "managed_nous_tools_enabled", lambda: False
    )

    result = json.loads(
        image_generation_tool.image_generate_tool(prompt="a cat")
    )

    assert result["success"] is False
    assert "https://fal.ai" in result["error"]
    assert "FAL_KEY" in result["error"]
