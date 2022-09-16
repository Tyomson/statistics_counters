from datetime import date
from typing import List
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import base
from config import ErrorDetails


async def get_statistics(
        db: AsyncSession,
        start_date: date,
        end_date: date
) -> List:
    """
    Получение статистики по датам

    Args:
        db (AsyncSession): Сессия базы данных
        start_date (date): Дата начала
        end_date (date): Дата конца

    Returns:
        List: Список объеков статистики
    """
    db_statistics = await db.execute(select(base.Statistics).where(
        base.Statistics.created_dt >= start_date,
        base.Statistics.created_dt <= end_date,
    ).order_by(base.Statistics.created_dt.desc()))
    statistics = db_statistics.scalars().all()
    if not statistics:
        raise HTTPException(status_code=404, detail=ErrorDetails.NOT_FOUND)
    return statistics


async def created_statistics(
        db: AsyncSession,
        statistics_date: date,
) -> base.Statistics:
    """
    Создание объекта статистики.

    Args:
        db (AsyncSession): Сессия базы данных
        statistics_date (date): Дата статистики

    Returns:
        base.Statistics: Объект статистики
    """
    db_statistics = await db.execute(select(base.Statistics).where(
        base.Statistics.created_dt == statistics_date
    ))
    statistics = db_statistics.scalars().first()
    if statistics is None:
        statistics = base.Statistics(
            created_dt=statistics_date,
        )
        db.add(statistics)
        await db.commit()
        await db.refresh(statistics)
    return statistics


async def update_statistics(
        db: AsyncSession,
        statistics: base.Statistics,
        views: int = 0,
        clicks: int = 0,
        cost: Decimal = 0.0,
) -> base.Statistics:
    """
    Обновление объекта статистики.

    Args:
        db (AsyncSession): Сессия базы данных
        statistics (base.Statistics): Объект статистики
        views (int): Количество просмотров
        clicks (int): Количество кликов
        cost (int): Стоимость кликов

    Returns:
        base.Statistics: Объект статистики
    """
    statistics.views = views + statistics.views \
        if statistics.views is not None else views
    statistics.clicks = clicks + statistics.clicks \
        if statistics.clicks is not None else clicks
    statistics.cost = cost + statistics.cost \
        if statistics.cost is not None else cost
    await db.commit()
    return statistics


async def update_additionally_statistics(
        db: AsyncSession,
        statistics: base.Statistics,
) -> base.Statistics:
    """
    Обновление дополнительных столбцов объекта статистики.

    Args:
        db (AsyncSession): Сессия базы данных
        statistics (base.Statistics): Объект статистики

    Returns:
        base.Statistics: Объект статистики
    """
    if statistics.cost != 0 and statistics.clicks != 0:
        statistics.cpc = statistics.cost / statistics.clicks
    if statistics.cost != 0 and statistics.views != 0:
        statistics.cpm = round(statistics.cost / statistics.views * 1000, 2)
    await db.commit()
    return statistics


async def delete_statistics(
        db: AsyncSession,
):
    """
    Удаление статистики

    Args:
        db (AsyncSession): Сессия базы данных
    """
    db_statistics = await db.execute(select(base.Statistics))
    statistics = db_statistics.scalars()
    for statistic in statistics:
        await db.delete(statistic)
        await db.commit()
