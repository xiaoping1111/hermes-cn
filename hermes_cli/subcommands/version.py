
"""version子命令解析器

【产品经理理解要点】
hermes version子命令的argparse解析器构建。
- 版本信息子命令参数定义
- 从main.py提取（god-file Phase 2）
- 处理器通过依赖注入传入

────────────────────────────────────────────────────────────────"""

"""``hermes version`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.
"""

from __future__ import annotations

from typing import Callable


def build_version_parser(subparsers, *, cmd_version: Callable) -> None:
    """Attach the ``version`` subcommand to ``subparsers``."""
    # =========================================================================
    # version command
    # =========================================================================
    version_parser = subparsers.add_parser("version", help="Show version information")
    version_parser.set_defaults(func=cmd_version)
