"""Google Meet远程节点主机方案

【产品经理理解要点】
允许Meet机器人(Playwright+Chrome)运行在与网关不同的机器上。网关通过JSON-over-WebSocket RPC协议与远程节点通信。
- 拓扑：gateway ──ws://──▶ 节点服务器 └─▶ meet_bot(Playwright)
- 使用场景：Google登录+Chrome配置在用户笔记本上，远程运行避免传输凭证
- 核心组件：NodeClient(网关端RPC)、NodeServer(节点端服务器)、NodeRegistry(节点注册表)

─────────────────────────────────────────────────────────────────
Lets the Meet bot (Playwright + Chrome) run on a different machine than
the hermes-agent gateway. The gateway speaks a small JSON-over-WebSocket
RPC protocol to the remote node; the node wraps the existing
``plugins.google_meet.process_manager`` API.

Topology
--------
    gateway (Linux)  ── ws://mac.local:18789 ──▶  node server (Mac)
                                                  └─ process_manager
                                                     └─ meet_bot (Playwright)

Why: Google sign-in + Chrome profile live on the user's laptop. Running
the bot there reuses that profile without shipping credentials to the
server.

Public surface
--------------
    NodeClient     — gateway-side RPC client (short-lived sync WS per call)
    NodeServer     — long-running server that hosts the bot
    NodeRegistry   — local JSON registry of approved nodes (name → url+token)
    protocol       — message envelope helpers (make_request, encode, decode, ...)
"""

from __future__ import annotations

from plugins.google_meet.node import protocol
from plugins.google_meet.node.client import NodeClient
from plugins.google_meet.node.protocol import (
    VALID_REQUEST_TYPES,
    decode,
    encode,
    make_error,
    make_request,
    make_response,
    validate_request,
)
from plugins.google_meet.node.registry import NodeRegistry
from plugins.google_meet.node.server import NodeServer

__all__ = [
    "NodeClient",
    "NodeServer",
    "NodeRegistry",
    "protocol",
    "make_request",
    "make_response",
    "make_error",
    "encode",
    "decode",
    "validate_request",
    "VALID_REQUEST_TYPES",
]
