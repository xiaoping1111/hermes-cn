"""ACP适配器启动入口

【产品经理理解要点】
支持通过 `python -m acp_adapter` 命令直接启动ACP服务，是开发调试时的便捷入口。
- 核心职责：提供模块级启动方式，内部委托给entry模块的main函数

─────────────────────────────────────────────────────────────────
Allow running the ACP adapter as ``python -m acp_adapter``."""

from .entry import main

main()
