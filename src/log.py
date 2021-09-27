import logging
import logging.config
from typing import Callable

from src.conf import settings

LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {'format': '%(asctime)s %(levelname)8s [%(name)s] %(funcName)s:%(lineno)-4s %(message)s'},
    },
    'handlers': {
        'stdout_default': {
            'class': 'logging.StreamHandler',
            'level': settings.LOG_LEVEL,
            'formatter': 'simple',
            'stream': 'ext://sys.stdout',
        }
    },
    'loggers': {
        'root': {'level': settings.LOG_LEVEL_ROOT, 'propagate': False, 'handlers': ['stdout_default']},
        settings.PROJECT_NAME: {
            'level': settings.LOG_LEVEL_PROJECT_NAME,
            'propagate': False,
            'handlers': ['stdout_default'],
        },
    },
}


def make_logger(name: str) -> Callable:
    """
    Создавать логи
    Example:
        >>> get_logger = make_logger('emerald')
        >>> log = get_logger('emerald')
        >>> log.info('Example message')
    """

    def wrap(module_name: str) -> logging.Logger:
        log_name = '.'.join((name, module_name))
        return logging.getLogger(log_name)

    return wrap


logging.config.dictConfig(LOG_CONFIG)


get_logger = make_logger(settings.PROJECT_NAME)
