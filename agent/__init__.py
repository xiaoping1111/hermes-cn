"""Agent internals -- extracted modules from run_agent.py.

Agent 包初始化

【产品经理理解要点】
从 run_agent.py 提取的内部模块包，包含纯工具函数和自包含类。
- 核心职责：标记为 agent 内部包、预加载 jiter 原生扩展
- 关键业务概念：模块提取(decomposition)、内部包约定
- 在系统中的位置：agent/ 包的入口

─────────────────────────────────────────────────────────────────


These modules contain pure utility functions and self-contained classes
that were previously embedded in the 3,600-line run_agent.py. Extracting
them makes run_agent.py focused on the AIAgent orchestrator class.
"""

from . import jiter_preload as _jiter_preload  # noqa: F401
