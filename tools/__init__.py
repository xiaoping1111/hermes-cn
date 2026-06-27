#!/usr/bin/env python3
"""工具包命名空间

【产品经理理解要点】
工具子系统的顶层包入口，负责组织智能体可调用的所有工具模块。
- 核心职责：作为工具模块的命名空间容器，不主动加载具体工具，避免循环依赖
- 设计原则：延迟加载——导入 tools 包不会触发任何工具模块的初始化
- 调用方式：业务代码应直接导入具体子模块（如 from tools import browser_tool）
- 在系统中的位置：位于工具注册表（registry.py）和具体工具实现之间，是工具层的基础设施

─────────────────────────────────────────────────────────────────
Tools package namespace.

Keep package import side effects minimal. Importing ``tools`` should not
eagerly import the full tool stack, because several subsystems load tools while
``hermes_cli.config`` is still initializing.

Callers should import concrete submodules directly, for example:

    import tools.web_tools
    from tools import browser_tool

Python will resolve those submodules via the package path without needing them
to be re-exported here.
"""


def check_file_requirements():
    """File tools only require terminal backend availability."""
    from .terminal_tool import check_terminal_requirements

    return check_terminal_requirements()


__all__ = ["check_file_requirements"]
