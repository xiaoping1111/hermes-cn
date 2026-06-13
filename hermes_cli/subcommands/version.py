"""``hermes version`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.

【产品经理理解要点】
命令行界面——用户通过终端与Hermes交互的入口（version.py）
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
