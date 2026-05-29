"""QQBot 共享常量定义

【产品经理理解要点】
QQ 机器人平台的配置参数中心，集中管理所有超时时间、API 地址和消息类型等常量。
- 核心职责：统一存放各模块共用的数值常量，避免分散硬编码导致配置不一致
- 关键参数：API 超时30秒、文件上传超时120秒、消息最长4000字符、重连退避策略等
- 消息类型：文本(0)、Markdown(2)、媒体(7)、输入状态(6)，决定消息在 QQ 端的渲染方式
- 环境可配：QQ 门户域名可通过 QQ_PORTAL_HOST 环境变量覆盖，支持企业代理和测试环境

─────────────────────────────────────────────────────────────────
QQBot package-level constants shared across adapter, onboard, and other modules.
"""

from __future__ import annotations

import os

# ---------------------------------------------------------------------------
# QQBot adapter version — bump on functional changes to the adapter package.
# ---------------------------------------------------------------------------

QQBOT_VERSION = "1.1.0"

# ---------------------------------------------------------------------------
# API endpoints
# ---------------------------------------------------------------------------

# The portal domain is configurable via QQ_API_HOST for corporate proxies
# or test environments.  Default: q.qq.com (production).
PORTAL_HOST = os.getenv("QQ_PORTAL_HOST", "q.qq.com")

API_BASE = "https://api.sgroup.qq.com"
TOKEN_URL = "https://bots.qq.com/app/getAppAccessToken"
GATEWAY_URL_PATH = "/gateway"

# QR-code onboard endpoints (on the portal host)
ONBOARD_CREATE_PATH = "/lite/create_bind_task"
ONBOARD_POLL_PATH = "/lite/poll_bind_result"
QR_URL_TEMPLATE = (
    "https://q.qq.com/qqbot/openclaw/connect.html"
    "?task_id={task_id}&_wv=2&source=hermes"
)

# ---------------------------------------------------------------------------
# Timeouts & retry
# ---------------------------------------------------------------------------

DEFAULT_API_TIMEOUT = 30.0
FILE_UPLOAD_TIMEOUT = 120.0
CONNECT_TIMEOUT_SECONDS = 20.0

RECONNECT_BACKOFF = [2, 5, 10, 30, 60]
MAX_RECONNECT_ATTEMPTS = 100
RATE_LIMIT_DELAY = 60  # seconds
QUICK_DISCONNECT_THRESHOLD = 5.0  # seconds
MAX_QUICK_DISCONNECT_COUNT = 3

ONBOARD_POLL_INTERVAL = 2.0  # seconds between poll_bind_result calls
ONBOARD_API_TIMEOUT = 10.0

# ---------------------------------------------------------------------------
# Message limits
# ---------------------------------------------------------------------------

MAX_MESSAGE_LENGTH = 4000
DEDUP_WINDOW_SECONDS = 300
DEDUP_MAX_SIZE = 1000

# ---------------------------------------------------------------------------
# QQ Bot message types
# ---------------------------------------------------------------------------

MSG_TYPE_TEXT = 0
MSG_TYPE_MARKDOWN = 2
MSG_TYPE_MEDIA = 7
MSG_TYPE_INPUT_NOTIFY = 6

# ---------------------------------------------------------------------------
# QQ Bot file media types
# ---------------------------------------------------------------------------

MEDIA_TYPE_IMAGE = 1
MEDIA_TYPE_VIDEO = 2
MEDIA_TYPE_VOICE = 3
MEDIA_TYPE_FILE = 4
