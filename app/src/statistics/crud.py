from datetime import date
from typing import List
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

import base
from config import ErrorDetails


def get_statistics(
        db: Session,
        start_date: date,
        end_date: date
) -> List:
    """
    Получение статистики по датам

    Args:
        db (Session): Сессия базы данных
        start_date (date): Дата начала
        end_date (date): Дата конца

    Returns:
        List: Список объеков статистики
    """
    db_statistics = db.query(base.Statistics).filter(
        base.Statistics.created_dt >= start_date,
        base.Statistics.created_dt <= end_date,
    )
    if not db_statistics.all():
        raise HTTPException(status_code=404, detail=ErrorDetails.NOT_FOUND)
    return db_statistics.order_by(desc(base.Statistics.created_dt)).all()


def created_statistics(
        db: Session,
        statistics_date: date,
) -> base.Statistics:
    """
    Создание объекта статистики.

    Args:
        db (Session): Сессия базы данных
        statistics_date (date): Дата статистики

    Returns:
        base.Statistics: Объект статистики
    """
    db_statistics = db.query(base.Statistics).filter(
        base.Statistics.created_dt == statistics_date
    ).first()
    if db_statistics is None:
        db_statistics = base.Statistics(
            created_dt=statistics_date,
        )
        db.add(db_statistics)
        db.commit()
        db.refresh(db_statistics)
    return db_statistics


def update_statistics(
        db: Session,
        statistics: base.Statistics,
        views: int = 0,
        clicks: int = 0,
        cost: Decimal = 0.0,
) -> base.Statistics:
    """
    Обновление объекта статистики.

    Args:
        db (Session): Сессия базы данных
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
    db.commit()
    return statistics


def update_additionally_statistics(
        db: Session,
        statistics: base.Statistics,
) -> base.Statistics:
    """
    Обновление дополнительных столбцов объекта статистики.

    Args:
        db (Session): Сессия базы данных
        statistics (base.Statistics): Объект статистики

    Returns:
        base.Statistics: Объект статистики
    """
    if statistics.cost != 0 and statistics.clicks != 0:
        statistics.cpc = statistics.cost / statistics.clicks
    if statistics.cost != 0 and statistics.views != 0:
        statistics.cpm = statistics.cost / statistics.views * 1000
    db.commit()
    return statistics


def delete_statistics(
        db: Session,
):
    """
    Удаление статистики

    Args:
        db (Session): Сессия базы данных
    """
    db.query(base.Statistics).delete()
    db.commit()
