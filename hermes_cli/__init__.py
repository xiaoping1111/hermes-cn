"""Hermes CLI 包入口

【产品经理理解要点】
Hermes 命令行工具的入口模块，定义版本号并确保 Windows 终端使用 UTF-8 编码。
- 核心职责：初始化 CLI 包、声明版本号（0.14.0）、修复 Windows 中文输出乱码问题
- 关键概念：hermes chat 交互对话、hermes gateway 消息网关、hermes cron 定时任务
- 系统定位：用户通过本模块进入 Hermes 的所有命令行功能

─────────────────────────────────────────────────────────────────
Hermes CLI - Unified command-line interface for Hermes Agent.

Provides subcommands for:
- hermes chat          - Interactive chat (same as ./hermes)
- hermes gateway       - Run gateway in foreground
- hermes gateway start - Start gateway service
- hermes gateway stop  - Stop gateway service
- hermes setup         - Interactive setup wizard
- hermes status        - Show status of all components
- hermes cron          - Manage cron jobs
"""

import os
import sys

__version__ = "0.14.0"
__release_date__ = "2026.5.16"


def _ensure_utf8():
    """Force UTF-8 stdout/stderr on Windows to prevent UnicodeEncodeError.

    Windows services and terminals default to cp1252, which cannot encode
    box-drawing characters used in CLI output. This causes unhandled
    UnicodeEncodeError crashes on gateway startup.
    """
    if sys.platform != "win32":
        return
    os.environ.setdefault("PYTHONUTF8", "1")
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream is None:
            continue
        try:
            if getattr(stream, "encoding", "").lower().replace("-", "") != "utf8":
                new_stream = open(
                    stream.fileno(), "w", encoding="utf-8",
                    buffering=1, closefd=False,
                )
                setattr(sys, stream_name, new_stream)
        except (AttributeError, OSError):
            pass


_ensure_utf8()
