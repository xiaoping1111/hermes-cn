"""LSP测试辅助模块

【产品经理理解要点】
LSP（语言服务器协议）测试套件的公共辅助工具包。LSP是代码编辑器与语言分析工具之间的通信协议，本模块为所有LSP相关测试提供共享的pytest fixture和辅助函数。
- 验证Hermes与语言服务器（如Pyright、TypeScript Language Server）的集成是否正确
- 确保代码诊断（语法错误、类型错误）能准确反馈给AI代理

─────────────────────────────────────────────────────────────────
Original English docstring continues below...

Pytest helpers for LSP-related tests."""
