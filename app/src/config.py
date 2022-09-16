import os


class ErrorDetails:
    INVALID_DATE_ARGUMENT = 'Invalid date argument'
    NOT_FOUND = 'Entry not found'

    codes = {
        INVALID_DATE_ARGUMENT: 100,
        NOT_FOUND: 404,
    }
#os.environ['DB_URL'] = 'mysql+pymysql://bot:123password123@mysql/statistics_counter'
os.environ['DB_URL'] = 'mysql+asyncmy://bot:123password123@localhost/statistics_counter'
os.environ['SENTRY_URL'] = 'https://ed4acb5f0ddc4065a4cceb55b1570812@o1006475.ingest.sentry.io/6176443'

STAGE = {
    'db_url': os.environ['DB_URL'],
    'sentry_url': os.environ['SENTRY_URL'],
    'cors_allow_origins': ["*"],
    'cors_allow_credentials': True,
    'cors_allow_methods': ["*"],
    'cors_allow_headers': ["*"],
}

CONFIG = STAGE.copy()
