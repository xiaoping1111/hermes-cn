"""Docker部署测试 - zombie reaping

【产品经理理解要点】
Docker容器化部署：权限、网关、僵尸进程回收、不可变安装等运维正确性中的zombie reaping验证。
- 验证功能：zombie reaping功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：zombie reaping功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Harness: PID 1 must reap orphaned zombie processes.

tini (current PID 1) reaps zombies via its built-in subreaper behavior.
s6-overlay's ``/init`` (Phase 2 PID 1) does the same. This invariant is
required for long-running containers spawning subprocesses (subagents,
dashboard, dynamic gateways) — otherwise the process table fills with
defunct entries and eventually exhausts the kernel PID space.

Every ``docker exec`` here runs as the unprivileged ``hermes`` user
(via :func:`docker_exec_sh` in conftest); see the conftest module
docstring.
"""
from __future__ import annotations

import time

from tests.docker.conftest import docker_exec, docker_exec_sh, start_container, start_container


def test_orphan_zombies_reaped(
    built_image: str, container_name: str,
) -> None:
    """Spawn an orphan child that exits immediately. PID 1 must reap it."""
    start_container(built_image, container_name, cmd="sleep 60")

    # `( ( sleep 0.1 & ) & ); sleep 1` creates a grandchild detached from
    # the original docker exec session — it becomes an orphan reparented
    # to PID 1 in the container. When it exits, PID 1 must reap it.
    docker_exec_sh(
        container_name, "( ( sleep 0.1 & ) & ); sleep 1", timeout=10,
    )

    # Poll for zombies-absent instead of a fixed sleep: reaping is
    # asynchronous (SIGCHLD) and can lag on a loaded host.
    deadline = time.monotonic() + 10
    zombies = ["(never checked)"]
    while time.monotonic() < deadline:
        r = docker_exec(container_name, "ps", "axo", "stat,pid,comm")
        zombies = [
            line for line in r.stdout.split("\n")
            if line.strip().startswith("Z")
        ]
        if not zombies:
            break
        time.sleep(0.5)
    assert not zombies, f"Zombies not reaped by PID 1: {zombies}"