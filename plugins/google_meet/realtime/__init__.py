"""Google Meet 实时音频包

【产品经理理解要点】
Google Meet 实时音频处理子包。
- 实时音频流处理

─────────────────────────────────────────────────────────────────
Realtime speech subpackage for the google_meet plugin (v2).

Provides a thin OpenAI Realtime API client and a file-queue speaker
wrapper so the Meet bot can play synthesized speech through the
virtual audio bridge.
"""

from .openai_client import RealtimeSession, RealtimeSpeaker  # noqa: F401

__all__ = ["RealtimeSession", "RealtimeSpeaker"]
