from datetime import date, timedelta

import pytest
import requests
from sqlalchemy import text

from test.utils import headers, url

TEST_STATISTICS_DATA = {
    'date': f"{(date.today() + timedelta(days=1)).strftime('%Y-%d-%m')}",
    'views': 10,
    'clicks': 10,
    'cost': 10.10,
}


class TestStatisticsGet:
    def test_statistics(self, get_test_statistics):
        test_statistics = get_test_statistics
        params = {
            'start_date': date.today().strftime('%Y-%d-%m'),
            'end_date': (date.today() + timedelta(days=10)).strftime('%Y-%d-%m'),
        }
        response = requests.get(f'{url}/statistics/', params=params, headers=headers)
        assert response.status_code == 200
        response_data = response.json()
        assert 'created_dt' in response_data[0]
        assert 'views' in response_data[0]


class TestStatisticsPost:
    def test_statistics_create(self, clean_user_client):
        response = clean_user_client.post(f'{url}/statistics/', json=TEST_STATISTICS_DATA, headers=headers)
        assert response.status_code == 201
        response_data = response.json()
        assert 'created_dt' in response_data
        assert 'views' in response_data


@pytest.fixture
def clean_user_client(get_test_db):
    db = get_test_db
    yield requests
    db.execute(text(
        f"""
        DELETE FROM statistics
        WHERE created_dt = '{(date.today() + timedelta(days=1)).strftime('%Y-%d-%m')}'
        """
    ))
    db.commit()
