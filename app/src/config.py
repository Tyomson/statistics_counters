import os


class ErrorDetails:
    INVALID_DATE_ARGUMENT = 'Invalid date argument'
    NOT_FOUND = 'Entry not found'

    codes = {
        INVALID_DATE_ARGUMENT: 100,
        NOT_FOUND: 404,
    }

STAGE = {
    'db_url': os.environ['DB_URL'],
    'sentry_url': os.environ['SENTRY_URL'],
    'cors_allow_origins': ["*"],
    'cors_allow_credentials': True,
    'cors_allow_methods': ["*"],
    'cors_allow_headers': ["*"],
}

CONFIG = STAGE.copy()
