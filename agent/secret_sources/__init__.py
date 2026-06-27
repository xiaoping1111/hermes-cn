"""External secret source integrations.

外部秘密来源集成

【产品经理理解要点】
管理外部凭据源(如 Bitwarden)，在进程启动时补充 .env 中缺少的变量。
- 核心职责：统一外部凭据源接口、非破坏性设置(不覆盖已有 .env 值)
- 关键业务概念：秘密源、非破坏性注入、Bitwarden
- 在系统中的位置：启动时凭据补充层

─────────────────────────────────────────────────────────────────


A secret source is anything that can supply environment-variable-shaped
credentials at process startup, _after_ ~/.hermes/.env has loaded.  By
default sources are non-destructive: they only set values for env vars
that aren't already present, so .env and shell exports continue to win.

Currently shipped:

  - ``bitwarden`` — Bitwarden Secrets Manager (`bws` CLI).  See
    ``agent.secret_sources.bitwarden`` for the integration and
    ``hermes_cli.secrets_cli`` for the user-facing setup wizard.
"""
