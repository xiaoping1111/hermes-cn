"""CLIdoctor dedicated provider skip测试

【产品经理理解要点】
CLIdoctor dedicated provider skip功能测试。
- 验证功能：命令行doctor dedicated provider skip功能
- 关键场景：配置、执行、验证
- 业务影响：doctor dedicated provider skip命令行功能失效

─────────────────────────────────────────────────────────────────────────
Regression: hermes doctor must not run a generic Bearer-auth health
check for providers that already have a dedicated check (Anthropic,
OpenRouter, Bedrock).

Anthropic's native API requires `x-api-key` + `anthropic-version` headers;
the generic loop sends `Authorization: Bearer ...` which Anthropic answers
with HTTP 404. The dedicated check at hermes_cli/doctor.py already covers
Anthropic with the right headers, so the pluggable profile must be
skipped by `_build_apikey_providers_list()`.

See: NousResearch/hermes-agent#22346"""

from __future__ import annotations


def test_build_apikey_providers_list_skips_dedicated_check_providers():
    from hermes_cli import doctor

    # Force a rebuild — the module caches the list on first call.
    doctor._APIKEY_PROVIDERS_CACHE = None
    entries = doctor._build_apikey_providers_list()

    # Tuple shape: (display_name, env_vars, default_url, base_env, supports_health_check)
    names = {entry[0].lower() for entry in entries}
    assert not any("anthropic" in name for name in names), (
        f"Anthropic provider profile leaked into generic Bearer-auth health "
        f"check loop. Dedicated check above already covers it with "
        f"x-api-key headers. Got entries: {sorted(names)}"
    )
    assert not any("openrouter" in name for name in names), (
        f"OpenRouter has a dedicated check; generic loop must skip it. "
        f"Got: {sorted(names)}"
    )
    assert not any("bedrock" in name for name in names), (
        f"Bedrock uses AWS SDK creds, not Bearer auth; generic loop must skip. "
        f"Got: {sorted(names)}"
    )


