"""Dashboard认证框架

【产品经理理解要点】
Dashboard认证提供者框架，非本地绑定且非insecure模式时启用。
- 多Provider插件注册机制
- Nous为默认Provider，第三方可通过插件注册
- 与Dashboard网关绑定的安全访问控制

────────────────────────────────────────────────────────────────
Dashboard authentication provider framework.

The dashboard auth gate engages only when the dashboard binds to a
non-loopback host without ``--insecure``. In that mode, every request must
carry a verified session from one of the registered ``DashboardAuthProvider``
plugins.

The Nous provider lives in ``plugins/dashboard-auth-nous/`` and is the
default. Third parties register their own providers via the plugin hook
``ctx.register_dashboard_auth_provider``."""
from hermes_cli.dashboard_auth.base import (
    DashboardAuthProvider,
    Session,
    LoginStart,
    InvalidCodeError,
    InvalidCredentialsError,
    ProviderError,
    RefreshExpiredError,
    assert_protocol_compliance,
)
from hermes_cli.dashboard_auth.registry import (
    register_provider,
    get_provider,
    list_providers,
    clear_providers,
)

__all__ = [
    "DashboardAuthProvider",
    "Session",
    "LoginStart",
    "InvalidCodeError",
    "InvalidCredentialsError",
    "ProviderError",
    "RefreshExpiredError",
    "assert_protocol_compliance",
    "register_provider",
    "get_provider",
    "list_providers",
    "clear_providers",
]
