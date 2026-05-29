"""路径安全验证 — 防止路径遍历攻击

【产品经理理解要点】
防止 AI 或恶意输入通过 "../" 等路径遍历手段访问不该访问的文件。
所有涉及文件路径的工具都应使用这个模块验证路径合法性。

─────────────────────────────────────────────────────────────────

Shared path validation helpers for tool implementations.

Extracts the ``resolve() + relative_to()`` and ``..`` traversal check
patterns previously duplicated across skill_manager_tool, skills_tool,
skills_hub, cronjob_tools, and credential_files.
"""

import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def validate_within_dir(path: Path, root: Path) -> Optional[str]:
    """Ensure *path* resolves to a location within *root*.

    Returns an error message string if validation fails, or ``None`` if the
    path is safe.  Uses ``Path.resolve()`` to follow symlinks and normalize
    ``..`` components.

    Usage::

        error = validate_within_dir(user_path, allowed_root)
        if error:
            return json.dumps({"error": error})
    """
    try:
        resolved = path.resolve()
        root_resolved = root.resolve()
        resolved.relative_to(root_resolved)
    except (ValueError, OSError) as exc:
        return f"Path escapes allowed directory: {exc}"
    return None


def has_traversal_component(path_str: str) -> bool:
    """Return True if *path_str* contains ``..`` traversal components.

    Quick check for obvious traversal attempts before doing full resolution.
    """
    parts = Path(path_str).parts
    return ".." in parts
