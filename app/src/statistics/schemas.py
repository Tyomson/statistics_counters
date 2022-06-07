from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class StatisticsBase(BaseModel):
    """Базовая модель статистики"""

    created_dt: date
    views: Optional[int]
    clicks: Optional[int]
    cost: Optional[Decimal]


class StatisticsRelated(StatisticsBase):
    """Модель возвращаемой статистики"""

    cpc: Optional[Decimal]
    cpm: Optional[Decimal]

    class Config:
        orm_mode = True


class StatisticsCreate(BaseModel):
    """Модель создания объекта статистики"""

    date: date
    views: Optional[int]
    clicks: Optional[int]
    cost: Optional[Decimal]

