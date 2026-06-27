"""ACP 模块入口

【产品经理理解要点】
支持通过 `python -m acp_adapter` 命令直接启动 ACP 适配器。
- 核心职责：作为 Python 包的命令行入口点，调用 entry 模块的 main 函数
- 系统定位：启动引导层，串联命令行与 ACP 服务

─────────────────────────────────────────────────────────────────
Allow running the ACP adapter as ``python -m acp_adapter``."""

from .entry import main

main()
