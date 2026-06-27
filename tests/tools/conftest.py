"""工具系统测试 - conftest

【产品经理理解要点】
工具层（MCP/浏览器/文件/图片/搜索/终端/TTS/审批等）的安全性与功能正确性中的conftest验证。
- 验证功能：conftest功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：conftest功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Shared fixtures for tests/tools/ web-provider tests.

Per-file subprocess isolation means each test file gets a fresh interpreter,
so module-level state (like the web-search-provider registry) is empty when
a file starts.  The ``web_registry_populated`` fixture registers all bundled
providers before each test and resets the registry afterwards — tests that
depend on the registry being populated should use it explicitly or via
``@pytest.mark.usefixtures("web_registry_populated")``.
"""

from unittest.mock import patch

import pytest


def register_all_web_providers():
    """Register all bundled web-search providers into the global registry.

    This is the single source of truth for the provider list used by
    test classes that need the registry populated for dispatch checks.
    """
    from agent.web_search_registry import register_provider, _reset_for_tests
    from plugins.web.brave_free.provider import BraveFreeWebSearchProvider
    from plugins.web.ddgs.provider import DDGSWebSearchProvider
    from plugins.web.exa.provider import ExaWebSearchProvider
    from plugins.web.firecrawl.provider import FirecrawlWebSearchProvider
    from plugins.web.parallel.provider import ParallelWebSearchProvider
    from plugins.web.searxng.provider import SearXNGWebSearchProvider
    from plugins.web.tavily.provider import TavilyWebSearchProvider
    from plugins.web.xai.provider import XAIWebSearchProvider

    _reset_for_tests()
    for cls in (
        BraveFreeWebSearchProvider,
        DDGSWebSearchProvider,
        ExaWebSearchProvider,
        FirecrawlWebSearchProvider,
        ParallelWebSearchProvider,
        SearXNGWebSearchProvider,
        TavilyWebSearchProvider,
        XAIWebSearchProvider,
    ):
        register_provider(cls())


@pytest.fixture
def web_registry_populated():
    """Populate the web-search-provider registry for one test, then reset."""
    register_all_web_providers()
    yield
    from agent.web_search_registry import _reset_for_tests
    _reset_for_tests()


@pytest.fixture
def disable_lazy_stt_install():
    """Disarm the runtime lazy-install probe so static ``_HAS_FASTER_WHISPER``
    patches accurately simulate 'faster-whisper not installed'.

    Without this, ``_try_lazy_install_stt()`` calls
    ``importlib.util.find_spec("faster_whisper")``, which returns truthy
    whenever the package is installed in the dev / CI environment —
    defeating the test's ``_HAS_FASTER_WHISPER=False`` patch.

    Opt in at module scope with
    ``pytestmark = pytest.mark.usefixtures("disable_lazy_stt_install")``.
    """
    with patch("tools.transcription_tools._try_lazy_install_stt", return_value=False):
        yield
