"""共享 ANSI 颜色工具

【产品经理理解要点】
为 CLI 各模块提供统一的终端彩色输出能力，自动尊重 NO_COLOR 环境变量。
- 核心职责：判断是否应使用彩色输出（NO_COLOR/TERM=dumb/非 TTY 时禁用），提供标准 ANSI 颜色常量
- 关键概念：NO_COLOR 标准（https://no-color.org/）、TTY 检测、ANSI 转义码
- 系统定位：CLI 展示层的基础工具，所有终端彩色输出都通过本模块

─────────────────────────────────────────────────────────────────
Shared ANSI color utilities for Hermes CLI modules."""

import os
import sys


def should_use_color() -> bool:
    """Return True when colored output is appropriate.

    Respects the NO_COLOR environment variable (https://no-color.org/)
    and TERM=dumb, in addition to the existing TTY check.
    """
    if os.environ.get("NO_COLOR") is not None:
        return False
    if os.environ.get("TERM") == "dumb":
        return False
    if not sys.stdout.isatty():
        return False
    return True


class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"


def color(text: str, *codes) -> str:
    """Apply color codes to text (only when color output is appropriate)."""
    if not should_use_color():
        return text
    return "".join(codes) + text + Colors.RESET
