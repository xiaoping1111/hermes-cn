"""命令行界面测试 - gateway·platform·门控策略

【产品经理理解要点】
验证命令行界面的门控策略功能
- 验证的功能: Host-specific gating in ``hermes_cli.gateway._all_platforms()``
- 核心测试场景: matrix present on linux、matrix present on macos、matrix hidden on windows 等共4个场景
- 业务影响: CLI命令可能出现异常，影响用户配置和操作体验

─────────────────────────────────────────────────────────────────
Host-specific gating in ``hermes_cli.gateway._all_platforms()``.

Some messaging platforms can't function on every host. The gate lives
in one place — ``_all_platforms()`` — so the setup wizard, the curses
gateway-config menu, and any future picker all see the same filtered
list.

Currently:
- Matrix is hidden on Windows. The ``[matrix]`` extra pulls
  ``mautrix[encryption]`` -> ``python-olm``, which has no Windows wheel
  and needs ``make`` + libolm to build from sdist. There's no native
  Windows path that works.
"""

import sys


class TestMatrixHiddenOnWindows:
    def test_matrix_present_on_linux(self, monkeypatch):
        """Sanity: matrix is still in the picker on Linux/macOS."""
        import hermes_cli.gateway as gateway_mod

        monkeypatch.setattr(gateway_mod.sys, "platform", "linux")
        platforms = gateway_mod._all_platforms()
        keys = {p["key"] for p in platforms}
        assert "matrix" in keys, "matrix must be available on Linux"

    def test_matrix_present_on_macos(self, monkeypatch):
        import hermes_cli.gateway as gateway_mod

        monkeypatch.setattr(gateway_mod.sys, "platform", "darwin")
        platforms = gateway_mod._all_platforms()
        keys = {p["key"] for p in platforms}
        assert "matrix" in keys, "matrix must be available on macOS"

    def test_matrix_hidden_on_windows(self, monkeypatch):
        """The actual gate: matrix must NOT appear on Windows."""
        import hermes_cli.gateway as gateway_mod

        monkeypatch.setattr(gateway_mod.sys, "platform", "win32")
        platforms = gateway_mod._all_platforms()
        keys = {p["key"] for p in platforms}
        assert "matrix" not in keys, (
            "matrix must be hidden on Windows — python-olm has no "
            "Windows wheel and no native build path"
        )

    def test_other_platforms_unaffected_on_windows(self, monkeypatch):
        """Gating must only drop matrix, not collateral damage."""
        import hermes_cli.gateway as gateway_mod

        monkeypatch.setattr(gateway_mod.sys, "platform", "win32")
        platforms = gateway_mod._all_platforms()
        keys = {p["key"] for p in platforms}
        # A representative sample of platforms that have no Windows
        # blockers — picker should still surface them.
        for must_have in ("telegram", "discord", "slack", "mattermost"):
            assert must_have in keys, (
                f"{must_have} disappeared from Windows picker — gate is "
                "over-filtering"
            )
