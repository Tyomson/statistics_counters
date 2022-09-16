from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from statistics import schemas, crud
from base import get_session
from utils import get_query_dates

router = APIRouter(
    prefix='/statistics',
    tags=['statistics'],
)


@router.get(
    '/',
    response_model=List[schemas.StatisticsRelated],
    summary='Getting statistics',
    response_description='List of statistics by date',
)
async def get_statistics_list(
        start_date: str,
        end_date: str,
        db: AsyncSession = Depends(get_session)
):
    """
    Getting a list of statistics.
    The method accepts the following search string parameters:

    - **start_date**: The start date of the request in the format YYYY-MM-DD (string)
    - **end_date**: The end date of the request in the format YYYY-MM-DD (string)

    Returns statistics objects
    """
    start_date, end_date = get_query_dates(start_date, end_date)
    db_statistics = await crud.get_statistics(
        db=db,
        start_date=start_date,
        end_date=end_date
    )
    return db_statistics


@router.post(
    '/',
    response_model=schemas.StatisticsRelated,
    status_code=status.HTTP_201_CREATED,
    summary='Creating statistics',
    response_description='Created statistics object',
)
async def create_statistics(
        statistics: schemas.StatisticsCreate,
        db: AsyncSession = Depends(get_session)
):
    """
    Creating statistics. If there is already data for the date of entering statistics,
        then they are updated.
    Accepts a JSON object with the following parameters:

    - **date**: Date of statistics in the format (YYYY-MM-DD)(date)
    - **views**: Number of impressions (int)(Optional parameter)
    - **clicks**: Number of clicks (int)(Optional parameter)
    - **cost**: Cost of clicks (Decimal(10, 2))(Optional parameter)

    Returns a created or updated statistics object.
    """
    db_statistics = await crud.created_statistics(db, statistics.date)
    update_statistics = await crud.update_statistics(
        db,
        db_statistics,
        statistics.views,
        statistics.clicks,
        statistics.cost
    )
    additionally_statistics = await crud.update_additionally_statistics(
        db,
        update_statistics
    )
    return additionally_statistics


@router.delete(
    '/',
    summary='Deleting statistics',
    response_description='Result Message',
)
async def delete_statistics(
        db: AsyncSession = Depends(get_session)
):
    """
    Deleting statistics.

    Returns a message about the result
    """
    await crud.delete_statistics(db)
    return {'status': 'success'}

