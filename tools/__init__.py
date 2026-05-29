#!/usr/bin/env python3
"""工具包命名空间

【产品经理理解要点】
这是所有工具的包入口。工具是 Agent 的"能力单元"，每个工具让 AI 能做一件事：
  - 读文件、写文件、搜索代码
  - 执行终端命令
  - 搜索网页、提取网页内容
  - 管理记忆、管理技能
  - 生成图片、生成视频
  - 浏览器自动化
  - 等等40+种工具

工具通过 registry.register() 自动注册，AI 根据需要选择使用。
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
