"""ACP 协议适配器

【产品经理理解要点】
将 Hermes Agent 能力通过 ACP（Agent Communication Protocol）协议暴露给外部编辑器（如 Zed）。
- 核心职责：桥接 Hermes Agent 与 ACP 协议，让编辑器能直接调用 Agent 能力
- 关键概念：ACP 是一种标准化的智能体通信协议，类似 LSP（语言服务器协议）
- 系统定位：连接层——前端编辑器 ←ACP协议→ 本模块 ←内部API→ Hermes Agent

─────────────────────────────────────────────────────────────────
ACP (Agent Communication Protocol) adapter for hermes-agent."""
