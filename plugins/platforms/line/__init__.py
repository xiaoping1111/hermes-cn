"""LINE消息平台适配器插件入口

【产品经理理解要点】
LINE Messaging API插件的注册入口，将LINE适配器接入Hermes网关系统。
- 核心职责：注册LINE平台适配器到Hermes插件系统
- 平台能力：文本/图片/语音/视频收发、慢回复按钮、Loading动画
"""

from .adapter import register

__all__ = ["register"]
