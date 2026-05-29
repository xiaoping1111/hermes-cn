"""Google Meet实时语音子包(v2)

【产品经理理解要点】
v2实时语音能力的入口，提供OpenAI Realtime API客户端和文件队列扬声器，让Meet机器人能通过虚拟音频桥播放合成语音。
"""

from .openai_client import RealtimeSession, RealtimeSpeaker  # noqa: F401

__all__ = ["RealtimeSession", "RealtimeSpeaker"]
