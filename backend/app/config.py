import os


def get_database_url() -> str:
    """อ่าน URL ของฐานข้อมูลจากการตั้งค่าสภาพแวดล้อม"""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL must be set")
    return database_url
