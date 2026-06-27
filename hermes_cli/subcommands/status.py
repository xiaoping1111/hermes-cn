
"""status子命令解析器

【产品经理理解要点】
hermes status子命令的argparse解析器构建。
- 系统状态查看子命令参数定义
- 从main.py提取（god-file Phase 2）
- 处理器通过依赖注入传入

────────────────────────────────────────────────────────────────"""

"""``hermes status`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.
"""

from __future__ import annotations

from typing import Callable


def build_status_parser(subparsers, *, cmd_status: Callable) -> None:
    """Attach the ``status`` subcommand to ``subparsers``."""
    # =========================================================================
    # status command
    # =========================================================================
    status_parser = subparsers.add_parser(
        "status",
        help="Show status of all components",
        description="Display status of Hermes Agent components",
    )
    status_parser.add_argument(
        "--all", action="store_true", help="Show all details (redacted for sharing)"
    )
    status_parser.add_argument(
        "--deep", action="store_true", help="Run deep checks (may take longer)"
    )
    status_parser.set_defaults(func=cmd_status)
