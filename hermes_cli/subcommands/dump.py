
"""dump子命令解析器

【产品经理理解要点】
hermes dump子命令的argparse解析器构建。
- 信息导出子命令参数定义
- 从main.py提取（god-file Phase 2）
- 处理器通过依赖注入传入

────────────────────────────────────────────────────────────────"""

"""``hermes dump`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.
"""

from __future__ import annotations

from typing import Callable


def build_dump_parser(subparsers, *, cmd_dump: Callable) -> None:
    """Attach the ``dump`` subcommand to ``subparsers``."""
    # =========================================================================
    # dump command
    # =========================================================================
    dump_parser = subparsers.add_parser(
        "dump",
        help="Dump setup summary for support/debugging",
        description="Output a compact, plain-text summary of your Hermes setup "
        "that can be copy-pasted into Discord/GitHub for support context",
    )
    dump_parser.add_argument(
        "--show-keys",
        action="store_true",
        help="Show redacted API key prefixes (first/last 4 chars) instead of just set/not set",
    )
    dump_parser.set_defaults(func=cmd_dump)
