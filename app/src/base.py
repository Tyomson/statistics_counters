from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Numeric, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import CONFIG

SQLALCHEMY_DATABASE_URL = CONFIG['db_url']

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _get_date():
    return datetime.now()


class Statistics(Base):
    """Модель статистики"""

    __tablename__ = 'statistics'

    id = Column(Integer, primary_key=True)
    created_dt = Column(Date, default=_get_date)
    views = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    cost = Column(Numeric(precision=10, scale=2), default=0)
    cpc = Column(Numeric(precision=10, scale=2), default=0)
    cpm = Column(Numeric(precision=10, scale=2), default=0)
