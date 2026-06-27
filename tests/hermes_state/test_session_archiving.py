"""会话归档

【产品经理理解要点】
会话归档。
- 验证功能：会话历史归档处理
- 关键场景：归档触发、存储、检索、清理
- 业务影响：历史会话无法归档或检索"""

import time

import pytest

from hermes_state import SessionDB


@pytest.fixture
def db(tmp_path):
    database = SessionDB(tmp_path / "state.db")
    try:
        yield database
    finally:
        database.close()


def _compression_pair(db: SessionDB):
    base = time.time() - 100
    db.create_session("root", source="cli")
    db.create_session("tip", source="cli", parent_session_id="root")
    db._conn.execute(
        "UPDATE sessions SET started_at = ?, ended_at = ?, end_reason = 'compression', message_count = 1 WHERE id = 'root'",
        (base, base + 10),
    )
    db._conn.execute(
        "UPDATE sessions SET started_at = ?, message_count = 1 WHERE id = 'tip'",
        (base + 20,),
    )
    db._conn.commit()


def test_archiving_compression_tip_archives_projected_root(db):
    _compression_pair(db)

    assert db.set_session_archived("tip", True) is True

    assert db.get_session("root")["archived"] == 1
    assert db.get_session("tip")["archived"] == 1
    assert [s["id"] for s in db.list_sessions_rich(order_by_last_active=True)] == []
    assert [s["id"] for s in db.list_sessions_rich(order_by_last_active=True, archived_only=True)] == ["tip"]


def test_unarchiving_compression_tip_unarchives_projected_root(db):
    _compression_pair(db)
    db.set_session_archived("tip", True)

    assert db.set_session_archived("tip", False) is True

    assert db.get_session("root")["archived"] == 0
    assert db.get_session("tip")["archived"] == 0
    assert [s["id"] for s in db.list_sessions_rich(order_by_last_active=True)] == ["tip"]
