import logging.config

from sentry_sdk.integrations.logging import LoggingIntegration


dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "base"
        },
    },
    "loggers": {
        "main": {
            "level": "DEBUG",
            "handlers": ["console"],
        },
    },
}

sentry_logging = LoggingIntegration(
    level=logging.INFO,
    event_level=logging.ERROR,
)
