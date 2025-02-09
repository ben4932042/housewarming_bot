import logging
from logging import Logger

from app.settings.config import config


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(levelname)s %(module)s %(funcName)s %(lineno)s"
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        # default log setting
        "": {
            "handlers": ["default"],
            "level": f"{config.log_level}",
            "propagate": True,
        },
        # specific log setting
        "uvicorn": {
            "handlers": ["default"],
            "level": "ERROR",
        },
        "uvicorn.error": {
            "handlers": ["default"],
            "level": "ERROR",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["default"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}


def setup_logger() -> Logger:
    return logging.getLogger(__name__)