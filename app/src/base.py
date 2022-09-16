from datetime import datetime

from sqlalchemy import MetaData
from sqlalchemy import Column, Integer, Numeric, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


from config import CONFIG


SQLALCHEMY_DATABASE_URL = CONFIG['db_url']

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    #connect_args={"check_same_thread": True}
)
SessionLocal = sessionmaker(
    class_=AsyncSession,
    future=True,
    expire_on_commit=False,
    autoflush=False,
    bind=engine
)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': (
        'fk__%(table_name)s__%(all_column_names)s__'
        '%(referred_table_name)s'
    ),
    'pk': 'pk__%(table_name)s'
}
metadata = MetaData(naming_convention=convention)


def _get_date():
    return datetime.now()


class Statistics(Base):
    """Statistics model"""

    __tablename__ = 'statistics'

    id = Column(Integer, primary_key=True)
    created_dt = Column(Date, default=_get_date)
    views = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    cost = Column(Numeric(precision=10, scale=2), default=0)
    cpc = Column(Numeric(precision=10, scale=2), default=0)
    cpm = Column(Numeric(precision=10, scale=2), default=0)
