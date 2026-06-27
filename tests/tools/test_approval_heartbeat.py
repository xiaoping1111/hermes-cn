"""工具系统测试 - approval heartbeat

【产品经理理解要点】
工具层（MCP/浏览器/文件/图片/搜索/终端/TTS/审批等）的安全性与功能正确性中的approval heartbeat验证。
- 验证功能：approval heartbeat功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：approval heartbeat功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Tests for the activity-heartbeat behavior of the blocking gateway approval wait.

Regression test for false gateway inactivity timeouts firing while the agent
is legitimately blocked waiting for a user to respond to a dangerous-command
approval prompt.  Before the fix, ``entry.event.wait(timeout=...)`` blocked
silently — no ``_touch_activity()`` calls — and the gateway's inactivity
watchdog (``agent.gateway_timeout``, default 1800s) would kill the agent
while the user was still choosing whether to approve.

The fix polls the event in short slices and fires ``touch_activity_if_due``
between slices, mirroring ``_wait_for_process`` in ``tools/environments/base.py``.
"""

import os


def _clear_approval_state():
    """Reset all module-level approval state between tests."""
    from tools import approval as mod
    mod._gateway_queues.clear()
    mod._gateway_notify_cbs.clear()
    mod._session_approved.clear()
    mod._permanent_approved.clear()
    mod._pending.clear()


class TestApprovalHeartbeat:
    """The blocking gateway approval wait must fire activity heartbeats.

    Without heartbeats, the gateway's inactivity watchdog kills the agent
    thread while it's legitimately waiting for a slow user to respond to
    an approval prompt (observed in real user logs: MRB, April 2026).
    """

    SESSION_KEY = "heartbeat-test-session"

    def setup_method(self):
        _clear_approval_state()
        self._saved_env = {
            k: os.environ.get(k)
            for k in ("HERMES_GATEWAY_SESSION", "HERMES_YOLO_MODE",
                      "HERMES_SESSION_KEY")
        }
        os.environ.pop("HERMES_YOLO_MODE", None)
        os.environ["HERMES_GATEWAY_SESSION"] = "1"
        # The blocking wait path reads the session key via contextvar OR
        # os.environ fallback.  Contextvars don't propagate across threads
        # by default, so env var is the portable way to drive this in tests.
        os.environ["HERMES_SESSION_KEY"] = self.SESSION_KEY

    def teardown_method(self):
        for k, v in self._saved_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        _clear_approval_state()



