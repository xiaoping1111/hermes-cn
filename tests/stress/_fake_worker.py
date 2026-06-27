#!/usr/bin/env python3
"""压力与稳定性测试 -  fake worker

【产品经理理解要点】
高并发、竞态条件、模糊输入等极端场景下的系统健壮性中的 fake worker验证。
- 验证功能： fake worker功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响： fake worker功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Fake worker process that exercises the real subprocess contract.

Reads HERMES_KANBAN_TASK from env, heartbeats periodically, does short
work, completes via the CLI. Designed to be spawned by the dispatcher
exactly the way `hermes chat -q` would be, minus the LLM cost.
"""

import json
import os
import subprocess
import time


def main():
    tid = os.environ["HERMES_KANBAN_TASK"]
    workspace = os.environ.get("HERMES_KANBAN_WORKSPACE", "")

    # Announce via CLI (goes through real argparse + init_db + etc)
    subprocess.run(
        ["hermes", "kanban", "heartbeat", tid, "--note", "started"],
        check=True, capture_output=True,
    )

    # Simulate work with periodic heartbeats
    for i in range(3):
        time.sleep(0.3)
        subprocess.run(
            ["hermes", "kanban", "heartbeat", tid, "--note", f"progress {i+1}/3"],
            check=True, capture_output=True,
        )

    # Complete with structured handoff
    subprocess.run(
        [
            "hermes", "kanban", "complete", tid,
            "--summary", f"real-subprocess worker finished {tid}",
            "--metadata", json.dumps({
                "workspace": workspace,
                "worker_pid": os.getpid(),
                "iterations": 3,
            }),
        ],
        check=True, capture_output=True,
    )


if __name__ == "__main__":
    main()
