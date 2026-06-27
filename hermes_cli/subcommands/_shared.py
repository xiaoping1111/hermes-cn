
"""子命令共享工具

【产品经理理解要点】
多个子命令构建器共享的参数解析辅助函数。
- add_accept_hooks_flag等通用参数标志
- 从main.py提取以避免循环导入
- main.py重新导出以保持向后兼容

────────────────────────────────────────────────────────────────"""

"""Shared parser helpers used across multiple CLI subcommand builders.

These were module-level helpers in ``hermes_cli/main.py``. They are pulled
into a neutral module so both ``main.py`` and every
``hermes_cli/subcommands/<group>.py`` builder can import them without an
import cycle. ``main.py`` re-exports them for backwards compatibility, so
existing references keep working.
"""

from __future__ import annotations

import argparse


def add_accept_hooks_flag(parser: argparse.ArgumentParser) -> None:
    """Attach the ``--accept-hooks`` flag.

    Shared across every agent subparser so the flag works regardless of CLI
    position.
    """
    parser.add_argument(
        "--accept-hooks",
        action="store_true",
        default=argparse.SUPPRESS,
        help=(
            "Auto-approve unseen shell hooks without a TTY prompt "
            "(equivalent to HERMES_ACCEPT_HOOKS=1 / hooks_auto_accept: true)."
        ),
    )
