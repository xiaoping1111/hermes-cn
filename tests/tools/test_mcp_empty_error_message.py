"""工具系统测试 - mcp empty error message

【产品经理理解要点】
工具层（MCP/浏览器/文件/图片/搜索/终端/TTS/审批等）的安全性与功能正确性中的mcp empty error message验证。
- 验证功能：mcp empty error message功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：mcp empty error message功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Regression tests for MCP error messages when str(exc) is empty.

Issue #19417: ClosedResourceError (and similar exceptions raised without a
message argument) produced ``MCP call failed: ClosedResourceError: `` with
nothing after the colon, making debugging impossible.

Fix: ``_exc_str()`` falls back to ``repr(exc)`` when ``str(exc)`` is empty.
"""


from tools.mcp_tool import _exc_str, _sanitize_error


# ---------------------------------------------------------------------------
# _exc_str unit tests
# ---------------------------------------------------------------------------


class _EmptyMessageError(Exception):
    """Exception whose __str__ returns empty string (like anyio.ClosedResourceError)."""

    def __str__(self):
        return ""


class _NormalError(Exception):
    pass


def test_exc_str_returns_str_when_nonempty():
    exc = _NormalError("something broke")
    assert _exc_str(exc) == "something broke"


# ---------------------------------------------------------------------------
# Integration: error message format in _sanitize_error
# ---------------------------------------------------------------------------


def test_error_message_preserves_normal_exception_text():
    """Normal exceptions should still show their message text."""
    exc = _NormalError("connection refused")
    error_msg = _sanitize_error(
        f"MCP call failed: {type(exc).__name__}: {_exc_str(exc)}"
    )
    assert "connection refused" in error_msg
    assert "_NormalError" in error_msg
