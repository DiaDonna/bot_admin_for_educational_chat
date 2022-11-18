import logging
import logging.config


class LevelDebug(logging.Filter):
    def filter(self, record):
        return record.levelno >= 30


class LevelInfo(logging.Filter):
    def filter(self, record):
        return record.levelno <= 20


dictLogConfig = {
    "version": 1,
    "disable_existing_loggers": False,
    'filters': {
        "debug": {
            "()": LevelDebug,
        },
        "info": {
            "()": LevelInfo,
        },
    },
    "handlers": {
        "fileDebug": {
            "class": "logging.handlers.RotatingFileHandler",
            "mode": "a",
            "maxBytes": 5242880,
            "backupCount": 0,
            "delay": False,
            "formatter": "myFormatter",
            "filters": ["debug"],
            "filename": "logs/debug.log",
            "encoding": "utf-8"
        },
        "fileInfo": {
            "class": "logging.handlers.RotatingFileHandler",
            "mode": "a",
            "maxBytes": 5242880,
            "backupCount": 0,
            "delay": False,
            "formatter": "myFormatter",
            "filters": ["info"],
            "filename": "logs/info.log",
            "encoding": "utf-8"
        },

    },
    "loggers": {
        'file_log': {
            "handlers": [
                "fileDebug",
                "fileInfo",
            ],
            "level": "DEBUG",
        },
    },
    "formatters": {
        "myFormatter": {
            "format": "%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
            "datefmt": '%d-%m-%Y %H:%M:%S'
        }
    }
}

logger = logging.getLogger('file_log')
logging.config.dictConfig(dictLogConfig)
