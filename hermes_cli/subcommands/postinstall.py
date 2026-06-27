
"""postinstall子命令解析器

【产品经理理解要点】
hermes postinstall子命令的argparse解析器构建。
- 安装后自动配置子命令参数定义
- 从main.py提取（god-file Phase 2）
- 处理器通过依赖注入传入

────────────────────────────────────────────────────────────────"""

"""``hermes postinstall`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.
"""

from __future__ import annotations

from typing import Callable


def build_postinstall_parser(subparsers, *, cmd_postinstall: Callable) -> None:
    """Attach the ``postinstall`` subcommand to ``subparsers``."""
    # =========================================================================
    # postinstall command
    # =========================================================================
    postinstall_parser = subparsers.add_parser(
        "postinstall",
        help="Bootstrap non-Python deps for pip installs (node, browser, ripgrep, ffmpeg)",
        description="One-shot post-install for pip users. Installs system "
        "dependencies that pip cannot provide, then runs setup if needed.",
    )
    postinstall_parser.set_defaults(func=cmd_postinstall)
