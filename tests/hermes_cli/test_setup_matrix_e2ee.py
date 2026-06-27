"""CLIsetup matrix e2ee测试

【产品经理理解要点】
CLIsetup matrix e2ee功能测试。
- 验证功能：命令行setup matrix e2ee功能
- 关键场景：配置、执行、验证
- 业务影响：setup matrix e2ee命令行功能失效

─────────────────────────────────────────────────────────────────────────
Test that setup.py has shutil available for Matrix E2EE auto-install."""
import ast



def _parse_setup_imports():
    """Parse setup.py and return top-level import names."""
    with open("hermes_cli/setup.py") as f:
        tree = ast.parse(f.read())
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                names.add(alias.name)
    return names


class TestSetupShutilImport:
    def test_shutil_imported_at_module_level(self):
        """shutil must be imported at module level so setup_gateway can use it
        for the mautrix auto-install path."""
        names = _parse_setup_imports()
        assert "shutil" in names, (
            "shutil is not imported at the top of hermes_cli/setup.py. "
            "This causes a NameError when the Matrix E2EE auto-install "
            "tries to call shutil.which('uv')."
        )
