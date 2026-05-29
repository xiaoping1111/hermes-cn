"""定时任务系统 — 让 AI 按计划自动执行任务

【产品经理理解要点】
定时任务让 AI 能"定时做事"，比如：
  - 每天早上 9 点搜索新闻
  - 每周一总结上周工作
  - 2小时后提醒我开会

由网关守护进程每60秒检查一次是否有到期任务。
文件锁防止多个进程同时执行同一任务。

─────────────────────────────────────────────────────────────────

Cron job scheduling system for Hermes Agent.

This module provides scheduled task execution, allowing the agent to:
- Run automated tasks on schedules (cron expressions, intervals, one-shot)
- Self-schedule reminders and follow-up tasks
- Execute tasks in isolated sessions (no prior context)

Cron jobs are executed automatically by the gateway daemon:
    hermes gateway install    # Install as a user service
    sudo hermes gateway install --system  # Linux servers: boot-time system service
    hermes gateway            # Or run in foreground

The gateway ticks the scheduler every 60 seconds. A file lock prevents
duplicate execution if multiple processes overlap.
"""

from cron.jobs import (
    create_job,
    get_job,
    list_jobs,
    remove_job,
    update_job,
    pause_job,
    resume_job,
    trigger_job,
    JOBS_FILE,
)
from cron.scheduler import tick

__all__ = [
    "create_job",
    "get_job", 
    "list_jobs",
    "remove_job",
    "update_job",
    "pause_job",
    "resume_job",
    "trigger_job",
    "tick",
    "JOBS_FILE",
]
