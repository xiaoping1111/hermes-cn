"""临时目录测试

【产品经理理解要点】
验证工具系统模块中uses os tmpdir for session artifacts、prefers backend env tmpdir override、falls back to tempfile when tmp missing的正确性
- uses os tmpdir for session artifacts的正确性验证
- prefers backend env tmpdir override的正确性验证
- falls back to tempfile when tmp missing的正确性验证
- 影响工具系统的可靠性和功能正确性"""

from unittest.mock import patch

from tools.environments.local import LocalEnvironment


class TestLocalTempDir:
    def test_uses_os_tmpdir_for_session_artifacts(self, monkeypatch):
        monkeypatch.setenv("TMPDIR", "/data/data/com.termux/files/usr/tmp")
        monkeypatch.delenv("TMP", raising=False)
        monkeypatch.delenv("TEMP", raising=False)

        with patch.object(LocalEnvironment, "init_session", autospec=True, return_value=None):
            env = LocalEnvironment(cwd=".", timeout=10)

        assert env.get_temp_dir() == "/data/data/com.termux/files/usr/tmp"
        assert env._snapshot_path == f"/data/data/com.termux/files/usr/tmp/hermes-snap-{env._session_id}.sh"
        assert env._cwd_file == f"/data/data/com.termux/files/usr/tmp/hermes-cwd-{env._session_id}.txt"

    def test_prefers_backend_env_tmpdir_override(self, monkeypatch):
        monkeypatch.delenv("TMPDIR", raising=False)
        monkeypatch.delenv("TMP", raising=False)
        monkeypatch.delenv("TEMP", raising=False)

        with patch.object(LocalEnvironment, "init_session", autospec=True, return_value=None):
            env = LocalEnvironment(
                cwd=".",
                timeout=10,
                env={"TMPDIR": "/data/data/com.termux/files/home/.cache/hermes-tmp/"},
            )

        assert env.get_temp_dir() == "/data/data/com.termux/files/home/.cache/hermes-tmp"
        assert env._snapshot_path == (
            f"/data/data/com.termux/files/home/.cache/hermes-tmp/hermes-snap-{env._session_id}.sh"
        )
        assert env._cwd_file == (
            f"/data/data/com.termux/files/home/.cache/hermes-tmp/hermes-cwd-{env._session_id}.txt"
        )

    def test_falls_back_to_tempfile_when_tmp_missing(self, monkeypatch):
        monkeypatch.delenv("TMPDIR", raising=False)
        monkeypatch.delenv("TMP", raising=False)
        monkeypatch.delenv("TEMP", raising=False)

        with patch("tools.environments.local.os.path.isdir", return_value=False), \
             patch("tools.environments.local.os.access", return_value=False), \
             patch("tools.environments.local.tempfile.gettempdir", return_value="/cache/tmp"), \
             patch.object(LocalEnvironment, "init_session", autospec=True, return_value=None):
            env = LocalEnvironment(cwd=".", timeout=10)
            assert env.get_temp_dir() == "/cache/tmp"
            assert env._snapshot_path == f"/cache/tmp/hermes-snap-{env._session_id}.sh"
            assert env._cwd_file == f"/cache/tmp/hermes-cwd-{env._session_id}.txt"
