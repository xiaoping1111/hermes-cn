"""TUI 网关

【产品经理理解要点】
终端 UI（TUI）模式下的 JSON-RPC 网关，连接 Hermes Agent 后端与 Ink/TUI 前端。
- 核心职责：在 TUI 子进程中运行，通过 JSON-RPC 协议将 Agent 能力暴露给终端 UI
- 关键概念：支持 stdio 和 WebSocket 两种传输方式，事件/审批/斜杠命令均复用同一分发逻辑
- 系统定位：通信网关层，TUI 前端 ←JSON-RPC→ 本网关 ←内部API→ Hermes Agent
"""
