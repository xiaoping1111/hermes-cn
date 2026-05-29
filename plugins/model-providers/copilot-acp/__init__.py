"""【产品经理理解要点】
GitHub Copilot ACP（Agent Communication Protocol）提供商——通过外部ACP子进程与Copilot通信，不走标准传输层。由run_agent.py单独处理。
─────────────────────────────────────────────────────────────────
GitHub Copilot ACP provider profile.

copilot-acp uses an external ACP subprocess — NOT the standard
transport. api_mode="copilot_acp" is handled separately in run_agent.py.
The profile captures auth + endpoint metadata for registry migration.
"""

from providers import register_provider
from providers.base import ProviderProfile


class CopilotACPProfile(ProviderProfile):
    """GitHub Copilot ACP — external process, no REST models endpoint."""

    def fetch_models(
        self,
        *,
        api_key: str | None = None,
        timeout: float = 8.0,
    ) -> list[str] | None:
        """Model listing is handled by the ACP subprocess."""
        return None


copilot_acp = CopilotACPProfile(
    name="copilot-acp",
    aliases=("github-copilot-acp", "copilot-acp-agent"),
    api_mode="chat_completions",  # ACP subprocess uses chat_completions routing
    env_vars=(),  # Managed by ACP subprocess
    base_url="acp://copilot",  # ACP internal scheme
    auth_type="external_process",
)

register_provider(copilot_acp)
