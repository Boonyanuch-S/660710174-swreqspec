from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool


class Base(DeclarativeBase):
    pass


def create_database_engine(database_url: str):
    """สร้าง engine สำหรับฐานข้อมูลตาม CON-TECH-01 โดยรองรับฐานข้อมูลทดสอบ"""
    engine_options = {"future": True}
    if database_url.startswith("sqlite") and ":memory:" in database_url:
        engine_options.update(
            {
                "connect_args": {"check_same_thread": False},
                "poolclass": StaticPool,
            }
        )
    return create_engine(database_url, **engine_options)


def create_session_factory(engine) -> sessionmaker[Session]:
    """สร้าง session factory จาก engine ของฐานข้อมูล"""
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_session(factory: sessionmaker[Session]) -> Iterator[Session]:
    """เปิดและปิด session ให้ผู้เรียกใช้งานฐานข้อมูลอย่างเป็นระบบ"""
    session = factory()
    try:
        yield session
    finally:
        session.close()
