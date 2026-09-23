from sqlalchemy.engine import Engine

from app.db.session import Base


def upgrade(engine: Engine) -> None:
    """สร้างตารางจาก metadata กลางของระบบตาม CON-TECH-01"""
    Base.metadata.create_all(bind=engine)
