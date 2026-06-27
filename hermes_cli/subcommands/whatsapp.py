
"""whatsapp子命令解析器

【产品经理理解要点】
hermes whatsapp子命令的argparse解析器构建。
- WhatsApp集成子命令参数定义
- 从main.py提取（god-file Phase 2）
- 处理器通过依赖注入传入

────────────────────────────────────────────────────────────────"""

"""``hermes whatsapp`` subcommand parser.

Extracted verbatim from ``hermes_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.
"""

from __future__ import annotations

from typing import Callable


def build_whatsapp_parser(subparsers, *, cmd_whatsapp: Callable) -> None:
    """Attach the ``whatsapp`` subcommand to ``subparsers``."""
    # =========================================================================
    # whatsapp command
    # =========================================================================
    whatsapp_parser = subparsers.add_parser(
        "whatsapp",
        help="Set up WhatsApp integration",
        description="Configure WhatsApp and pair via QR code",
    )
    whatsapp_parser.set_defaults(func=cmd_whatsapp)
