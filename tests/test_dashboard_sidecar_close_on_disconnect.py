import re
"""测试 - dashboard sidecar close on disconnect

【产品经理理解要点】
功能验证中的dashboard sidecar close on disconnect验证。
- 验证功能：dashboard sidecar close on disconnect功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：dashboard sidecar close on disconnect功能异常或存在安全隐患"""

from pathlib import Path

CHAT_SIDEBAR = Path(__file__).resolve().parent.parent / "web/src/components/ChatSidebar.tsx"


def test_sidecar_session_create_requests_close_on_disconnect():
    """The sidecar must opt its session into close_on_disconnect so the gateway
    reaps the slash_worker on WS disconnect (the #21370/#21467 leak)."""
    source = CHAT_SIDEBAR.read_text(encoding="utf-8")
    call = re.search(r'"session\.create",\s*\{(.*?)\}', source, re.DOTALL)
    assert call, "sidecar session.create call not found"
    assert re.search(r"close_on_disconnect:\s*true", call.group(1))


def test_sidecar_session_create_scopes_profile():
    """The sidecar must pass the dashboard's selected profile so model/credential
    info matches the PTY child under profile-scoped chat."""
    source = CHAT_SIDEBAR.read_text(encoding="utf-8")
    call = re.search(r'"session\.create",\s*\{(.*?)\}\);', source, re.DOTALL)
    assert call, "sidecar session.create call not found"
    body = call.group(1)
    assert re.search(r"close_on_disconnect:\s*true", body)
    assert re.search(r'source:\s*"tool"', body)
    assert re.search(r"\.\.\.\(profile\s*\?\s*\{\s*profile\s*\}\s*:\s*\{\}\)", body)
