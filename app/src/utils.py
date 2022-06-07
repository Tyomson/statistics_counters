from datetime import datetime, date, timedelta

from fastapi import HTTPException

from config import ErrorDetails


def parse_date(date_str: str) -> date:
    try:
        return datetime.strptime(date_str, '%Y-%d-%m').date()
    except ValueError:
        raise HTTPException(status_code=400, detail=ErrorDetails.INVALID_DATE_ARGUMENT)


def get_query_dates(start_date_str: str, end_date_str: str):
    if end_date_str:
        end_date = parse_date(end_date_str)
    else:
        end_date = date.today()
    if start_date_str:
        start_date = parse_date(start_date_str)
    else:
        start_date = end_date - timedelta(days=30)
    return start_date, end_date
