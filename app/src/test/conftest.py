from datetime import date, timedelta

import pytest_asyncio
from sqlalchemy import text

from test.base import SessionLocal


@pytest_asyncio.fixture
def get_test_db():
    db = SessionLocal()
    yield db
    db.close()


@pytest_asyncio.fixture
def get_test_statistics(get_test_db):
    db = get_test_db
    db.execute(f"""
    INSERT INTO statistics
    (created_dt, views, clicks, cost)
    VALUES ('{(date.today() + timedelta(days=1)).strftime('%Y-%d-%m')}', 10, 10, 10)
    """)
    db.commit()
    db_statistics = db.execute(
        f"""
        SELECT * FROM statistics
        WHERE created_dt = '{(date.today() + timedelta(days=1)).strftime('%Y-%d-%m')}'
        """
    ).fetchone()
    yield db_statistics
    db.execute(text(
        f"""
        DELETE FROM statistics
        WHERE created_dt = '{(date.today() + timedelta(days=1)).strftime('%Y-%d-%m')}'
        """
    ))
    db.commit()
