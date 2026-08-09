"""========================================
看板通知

【产品经理理解要点】
看板通知器。
- 验证功能：Kanban看板变更通知
- 关键场景：变更检测、通知发送、订阅管理
- 业务影响：看板变更无通知

────────────────────────────────────────────────────────────────────────
========================================

Notifier polling stays active when another gateway owns dispatching.

Tests for the dispatch_in_gateway gate on _kanban_notifier_watcher.

- Non-dispatch gateways (dispatch_in_gateway=false) exit before opening any DB.
- HERMES_KANBAN_DISPATCH_IN_GATEWAY env var disables without loading config.
- Dispatch-owning gateways (dispatch_in_gateway=true) proceed past the gate."""

import asyncio
from unittest.mock import MagicMock, patch

from gateway.config import Platform
from gateway.run import GatewayRunner


def _make_runner(with_adapter=False):
    runner = GatewayRunner.__new__(GatewayRunner)
    runner._running = True
    runner.adapters = {Platform.TELEGRAM: MagicMock()} if with_adapter else {}
    runner._kanban_sub_fail_counts = {}
    return runner


def test_notifier_watcher_polls_without_dispatch_ownership():
    """A profile gateway still polls its profile-owned subscriptions."""
    runner = _make_runner(with_adapter=True)
    past_gate = []
    sleep_calls = []

    async def fake_sleep(delay):
        sleep_calls.append(delay)
        # Stop after the initial delay + first per-interval sleep so the loop
        # body runs exactly once.
        if len(sleep_calls) >= 2:
            runner._running = False

    async def fake_to_thread(fn, *args, **kwargs):
        return fn(*args, **kwargs)

    import hermes_cli.kanban_db as _kb

    with patch.object(
        _kb, "list_boards",
        side_effect=lambda *a, **kw: past_gate.append(True) or [],
    ):
        with patch("asyncio.sleep", side_effect=fake_sleep):
            with patch("asyncio.to_thread", side_effect=fake_to_thread):
                asyncio.run(runner._kanban_notifier_watcher())

    assert past_gate, (
        "gateways without the dispatch lock must still poll owned subscriptions"
    )
