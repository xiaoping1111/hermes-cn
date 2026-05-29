"""TUI网关包

【产品经理理解要点】
TUI（终端用户界面）网关，是Hermes在终端中运行时的后台服务进程。
- 核心职责：在TUI和Agent之间充当JSON-RPC通信桥梁
- 系统定位：TUI前端通过stdin/stdout与此网关交互，网关管理Agent生命周期
"""
