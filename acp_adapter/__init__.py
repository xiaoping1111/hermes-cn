"""ACP协议适配器

【产品经理理解要点】
ACP（Agent Communication Protocol）适配器，让Hermes Agent可以通过标准协议接入编辑器（如Zed）。
- 核心职责：将Hermes Agent的能力包装为ACP标准服务，供外部客户端调用
- 关键概念：ACP是编辑器与AI代理之间的通信桥梁，类似于LSP之于语言服务
- 系统定位：用户在Zed等编辑器中使用Hermes时，就是这个模块在幕后工作

─────────────────────────────────────────────────────────────────
ACP (Agent Communication Protocol) adapter for hermes-agent."""
