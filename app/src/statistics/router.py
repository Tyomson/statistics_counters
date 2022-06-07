from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from statistics import schemas, crud
from base import get_db
from utils import get_query_dates

router = APIRouter(
    prefix='/statistics',
    tags=['statistics'],
)


@router.get(
    '/',
    response_model=List[schemas.StatisticsRelated],
    summary='Получение статистики',
    response_description='Список статистики по датам',
)
async def get_statistics_list(
        start_date: str,
        end_date: str,
        db: Session = Depends(get_db)
):
    """
    Получение списка статистики.
    Метод принимает следующие параметры поисковой строки:

    - **start_date**: начальная дата запроса в формате YYYY-MM-DD (string)
    - **end_date**: конечная дата запроса в формате YYYY-MM-DD (string)

    Возвращает объекты статистики
    """
    start_date, end_date = get_query_dates(start_date, end_date)
    db_statistics = crud.get_statistics(
        db=db,
        start_date=start_date,
        end_date=end_date
    )
    return db_statistics


@router.post(
    '/',
    response_model=schemas.StatisticsRelated,
    status_code=status.HTTP_201_CREATED,
    summary='Создания статистики',
    response_description='Созданный объект статистики',
)
async def create_statistics(
        statistics: schemas.StatisticsCreate,
        db: Session = Depends(get_db)
):
    """
    Создание статистики. Если за дату внесения статистики уже есть данные, то они обновляются.
    Принимает JSON-объект со следующими параметрами:

    - **date**: Дата статистики в формате (YYYY-MM-DD)(date)
    - **views**: Количество показов (int)(Необязательный параметр)
    - **clicks**: Количество кликов (int)(Необязательный параметр)
    - **cost**: Стоимость кликов (Decimal(10, 2))(Необязательный параметр)

    Возвращает созданный или обновленный объект статистики.
    """
    db_statistics = crud.created_statistics(db, statistics.date)
    update_statistics = crud.update_statistics(
        db,
        db_statistics,
        statistics.views,
        statistics.clicks,
        statistics.cost
    )
    additionally_statistics = crud.update_additionally_statistics(
        db,
        update_statistics
    )
    return additionally_statistics


@router.delete(
    '/',
    summary='Удаление статистики',
    response_description='Сообщение о результате',
)
def delete_statistics(
        db: Session = Depends(get_db)
):
    """
    Удаление статистики.

    Возвращает сообщение о результате
    """
    crud.delete_statistics(db)
    return {'status': 'success'}

