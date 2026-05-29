"""Hermes执行环境后端 — 命令运行环境的统一入口

【产品经理理解要点】
本模块定义了AI智能体执行命令的不同环境选项，让同一个智能体可以在本地、Docker容器、远程服务器、云沙箱等多种环境中运行命令。
- 支持的环境类型：本地主机、Docker容器、SSH远程服务器、Singularity容器、Modal云沙箱、Vercel云沙箱、Daytona云沙箱
- 统一接口：所有环境都实现BaseEnvironment接口，上层代码无需关心底层差异
- 业务价值：按需选择安全隔离级别——本地最便捷、Docker最通用、云沙箱最安全

─────────────────────────────────────────────────────────────────
Hermes execution environment backends.

Each backend provides the same interface (BaseEnvironment ABC) for running
shell commands in a specific execution context: local, Docker, SSH,
Singularity, Modal, Daytona, or Vercel Sandbox. (Modal additionally has
direct and Nous-managed modes, selected via terminal.modal_mode.)

The terminal_tool.py factory (_create_environment) selects the backend
based on the TERMINAL_ENV configuration.
"""

from tools.environments.base import BaseEnvironment

__all__ = ["BaseEnvironment"]
