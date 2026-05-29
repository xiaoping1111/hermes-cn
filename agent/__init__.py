"""Agent 内部模块 —— 从 run_agent.py 中提取的子模块。

【产品经理理解要点 — agent/ 目录是 Hermes 的"大脑"】

目录结构说明：
  conversation_loop.py  —— 对话主循环（核心：用户提问→AI回答→执行工具→循环）
  agent_init.py         —— 代理初始化逻辑（连接模型、加载工具、设置上下文）
  prompt_builder.py     —— 系统提示词组装（告诉AI"你是谁、能用什么工具"）
  tool_executor.py      —— 工具执行器（并行/串行执行AI调用的工具）
  memory_manager.py     —— 记忆管理器（跨会话记住用户偏好和知识）
  context_compressor.py —— 上下文压缩器（对话太长时压缩历史，保留关键信息）
  error_classifier.py   —— 错误分类器（判断API错误类型，决定重试还是切换模型）
  background_review.py  —— 后台评审（对话结束后自动评审记忆和技能）
  display.py            —— 显示层（工具调用过程的可视化展示）
  tool_guardrails.py    —— 工具护栏（防止AI执行危险命令）

These modules contain pure utility functions and self-contained classes
that were previously embedded in the 3,600-line run_agent.py. Extracting
them makes run_agent.py focused on the AIAgent orchestrator class.
"""
