"""自定义错误类型

自定义错误类型

【产品经理理解要点】
定义 Hermes Agent 的自定义异常类。
- 核心职责：定义 SSLConfigurationError 等专用异常
- 关键业务概念：SSL 配置错误、自定义异常层次
- 在系统中的位置：全局异常定义

─────────────────────────────────────────────────────────────────
"""
class SSLConfigurationError(Exception):
    """Raised when SSL/TLS certificate bundle configuration fails."""
    pass


class EmptyStreamError(RuntimeError):
    """Raised when a provider closes a stream without yielding a response."""

    pass


class MoAPresetNotFoundError(ValueError):
    """Raised when a persisted MoA preset no longer exists in config."""
