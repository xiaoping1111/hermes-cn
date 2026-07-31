"""External secret source integrations.

外部秘密来源集成

【产品经理理解要点】
管理外部凭据源(如 Bitwarden)，在进程启动时补充 .env 中缺少的变量。
- 核心职责：统一外部凭据源接口、非破坏性设置(不覆盖已有 .env 值)
- 关键业务概念：秘密源、非破坏性注入、Bitwarden
- 在系统中的位置：启动时凭据补充层

─────────────────────────────────────────────────────────────────


A secret source is anything that can supply environment-variable-shaped
credentials at process startup, _after_ ~/.hermes/.env has loaded.

The contract every source implements is
:class:`agent.secret_sources.base.SecretSource`; the orchestrator that
runs the enabled sources (ordering, mapped-beats-bulk precedence,
first-claim-wins conflicts, ``override_existing`` semantics, provenance)
is :func:`agent.secret_sources.registry.apply_all`.  Multiple sources
can be enabled at once — see the registry module docstring for the
precedence ladder.  The atomic-write / 0600 / TTL disk-cache substrate
is shared across backends in ``agent.secret_sources._cache`` so the
security-sensitive bits live in exactly one place.

Currently bundled:

  - ``bitwarden`` — Bitwarden Secrets Manager (`bws` CLI).  See
    ``agent.secret_sources.bitwarden`` for the integration and
    ``hermes_cli.secrets_cli`` for the user-facing setup wizard.
  - ``onepassword`` — 1Password ``op://`` secret references (`op` CLI).
    See ``agent.secret_sources.onepassword`` for the integration and
    ``hermes_cli.onepassword_secrets_cli`` for the user-facing commands.

The bundled set is deliberately closed (policy mirrors memory
providers): new third-party secret managers ship as standalone plugin
repos that subclass ``SecretSource`` and register through
``PluginContext.register_secret_source()`` — they are NOT added to this
package.  A generic ``command`` source is a possible future exception;
OS keystores (Keychain/DPAPI/libsecret) are under discussion.
"""

from agent.secret_sources.base import (  # noqa: F401
    SECRET_SOURCE_API_VERSION,
    ErrorKind,
    FetchResult,
    SecretSource,
    is_valid_env_name,
    run_secret_cli,
    scrub_ansi,
)
