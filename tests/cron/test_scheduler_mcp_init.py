"""定时任务测试 - 调度器MCP初始化

【产品经理理解要点】
验证定时任务调度引擎调度器MCP初始化的正确性
- 验证的功能: Regression tests for MCP server availability in cron jobs
- 核心测试场景: no agent cron job does not initialize mcp
- 业务影响: 定时任务可能无法正确调度执行，影响自动化工作流的可靠性

─────────────────────────────────────────────────────────────────
Regression tests for MCP server availability in cron jobs.

Background
==========
``cron/scheduler.py:run_job()`` constructs ``AIAgent(...)`` directly without
calling ``discover_mcp_tools()`` — the initialization that CLI and gateway
paths do at startup. Cron jobs therefore never saw any MCP tools from
``mcp_servers`` in config.yaml. See #4219.

The fix inserts ``discover_mcp_tools()`` before the ``AIAgent(...)`` call,
wrapped in try/except so a broken MCP server can't kill an otherwise
working cron job. ``discover_mcp_tools`` is idempotent — subsequent ticks
short-circuit on already-connected servers.
"""

from __future__ import annotations

from unittest.mock import patch, MagicMock

import pytest






def test_no_agent_cron_job_does_not_initialize_mcp():
    """Cron jobs with no_agent=True are script-only — no AIAgent, no MCP
    tools needed. We must NOT pay the MCP init cost for those."""
    from cron import scheduler

    job = {
        "id": "noagent-job",
        "name": "noagent-job",
        "no_agent": True,
        "script": "/nonexistent/script.sh",
    }

    discover_called = []

    def fake_discover():
        discover_called.append(True)
        return []

    # _run_job_script returns (ok, output); make it fail cleanly so we
    # don't need a real script file.
    with patch("tools.mcp_tool.discover_mcp_tools", side_effect=fake_discover), \
         patch("cron.scheduler._run_job_script", return_value=(False, "no such file")):
        scheduler.run_job(job)

    assert not discover_called, (
        "discover_mcp_tools was called for a no_agent job — wasted MCP init "
        "for a script-only cron tick"
    )
