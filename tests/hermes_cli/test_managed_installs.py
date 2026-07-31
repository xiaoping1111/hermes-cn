"""CLImanaged installs测试

【产品经理理解要点】
CLImanaged installs功能测试。
- 验证功能：命令行managed installs功能
- 关键场景：配置、执行、验证
- 业务影响：managed installs命令行功能失效"""

from types import SimpleNamespace
from unittest.mock import patch

from hermes_cli.config import recommended_update_command
from hermes_cli.main import cmd_update
from tools.skills_hub import OptionalSkillSource


def test_recommended_update_command_defaults_to_hermes_update(monkeypatch):
    monkeypatch.delenv("HERMES_MANAGED", raising=False)

    # Also short-circuit the .managed marker path — CI runners may have an
    # ambient ~/.hermes/.managed if a prior test left HERMES_HOME pointing
    # somewhere with that marker, which would make get_managed_update_command()
    # return "Update your Nix flake input ..." instead of falling through to
    # detect_install_method().
    with patch("hermes_cli.config.get_managed_update_command", return_value=None), \
         patch("hermes_cli.config.detect_install_method", return_value="git"):
        assert recommended_update_command() == "hermes update"


def test_optional_skill_source_honors_env_override(monkeypatch, tmp_path):
    optional_dir = tmp_path / "optional-skills"
    optional_dir.mkdir()
    monkeypatch.setenv("HERMES_OPTIONAL_SKILLS", str(optional_dir))

    source = OptionalSkillSource()

    assert source._optional_dir == optional_dir
