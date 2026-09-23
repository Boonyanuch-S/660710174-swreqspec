import importlib
from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session

from app.db.session import Base, create_database_engine, create_session_factory


@pytest.fixture
def database_engine():
    """เตรียม SQLite in-memory สำหรับทดสอบ migration โดยไม่ใช้ฐานข้อมูลจริง"""
    engine = create_database_engine("sqlite:///:memory:")
    migration = importlib.import_module("app.db.migrations.001_init")
    migration.upgrade(engine)
    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture
def database_session(database_engine) -> Iterator[Session]:
    """เปิด session บนฐานข้อมูลทดสอบให้ test ใช้งาน"""
    session_factory = create_session_factory(database_engine)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()


def test_database_setup(database_engine):
    """ตรวจว่า engine และ migration พร้อมใช้กับฐานข้อมูลทดสอบ"""
    assert database_engine.dialect.name == "sqlite"
    assert inspect(database_engine).get_table_names() == list(Base.metadata.tables)
