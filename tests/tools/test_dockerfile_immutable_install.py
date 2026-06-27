"""工具系统测试 - dockerfile immutable install

【产品经理理解要点】
工具层（MCP/浏览器/文件/图片/搜索/终端/TTS/审批等）的安全性与功能正确性中的dockerfile immutable install验证。
- 验证功能：dockerfile immutable install功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：dockerfile immutable install功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Contract tests for the Docker image's immutable /opt/hermes install tree.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCKERFILE = REPO_ROOT / "Dockerfile"


def _dockerfile_text() -> str:
    return DOCKERFILE.read_text()


def test_dockerfile_makes_opt_hermes_root_owned_and_non_writable() -> None:
    text = _dockerfile_text()

    assert "COPY --chown=hermes:hermes . ." not in text
    assert "COPY . ." in text
    assert "chown -R root:root /opt/hermes" in text
    assert "chmod -R a+rX /opt/hermes" in text
    assert "chmod -R a-w /opt/hermes" in text

    immutable_block = re.search(
        r"RUN mkdir -p /opt/hermes/bin && \\\n"
        r"(?:.*\\\n)+?"
        r"\s+chmod -R a-w /opt/hermes",
        text,
    )
    assert immutable_block, "Dockerfile must lock /opt/hermes after installing code/deps"


def test_dockerfile_keeps_mutable_state_under_opt_data() -> None:
    text = _dockerfile_text()

    assert "ENV HERMES_HOME=/opt/data" in text
    assert "ENV HERMES_WRITE_SAFE_ROOT=/opt/data" in text
    assert 'VOLUME [ "/opt/data" ]' in text


def test_dockerfile_disables_runtime_install_mutations() -> None:
    text = _dockerfile_text()

    assert "ENV PYTHONDONTWRITEBYTECODE=1" in text
    assert "ENV HERMES_DISABLE_LAZY_INSTALLS=1" in text
    assert "HERMES_TUI_DIR=/opt/hermes/ui-tui" in text


def test_dockerfile_does_not_chown_install_trees_to_hermes() -> None:
    text = _dockerfile_text()
    forbidden_patterns = (
        r"chown\s+-R\s+hermes:hermes\s+/opt/hermes/\.venv",
        r"chown\s+-R\s+hermes:hermes\s+/opt/hermes/ui-tui",
        r"chown\s+-R\s+hermes:hermes\s+/opt/hermes/gateway",
        r"chown\s+-R\s+hermes:hermes\s+/opt/hermes/node_modules",
    )
    for pattern in forbidden_patterns:
        assert not re.search(pattern, text), (
            "runtime install trees under /opt/hermes must stay immutable; "
            f"found forbidden pattern {pattern!r}"
        )


def test_dockerfile_bakes_code_scoped_install_method_stamp() -> None:
    """The 'docker' install-method stamp is baked next to the code.

    detect_install_method() reads the code-scoped stamp
    (/opt/hermes/.install_method) first; baking it at build time keeps the
    published image self-identifying as 'docker' WITHOUT writing into the
    shared $HERMES_HOME data volume (which a host install may also use).
    It must live inside the immutable block so the runtime user can't alter it.
    """
    text = _dockerfile_text()
    assert "printf 'docker\\n' > /opt/hermes/.install_method" in text

    immutable_block = re.search(
        r"RUN mkdir -p /opt/hermes/bin && \\\n"
        r"(?:.*\\\n)+?"
        r"\s+chmod -R a-w /opt/hermes",
        text,
    )
    assert immutable_block, "immutable block must exist"
    assert ".install_method" in immutable_block.group(0), (
        "the code-scoped install-method stamp must be baked inside the "
        "immutable /opt/hermes block"
    )
