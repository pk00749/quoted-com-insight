import logging
import logging.config
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


def configure_logging(log_level: str = "INFO", log_path: Optional[str] = None):
    """Configure console + rotating file logging. Ensures log directory exists.

    Falls back to console-only logging if file handler cannot be initialized.
    """
    level = (log_level or "INFO").upper()
    handlers = ["console"]

    file_handler_config = None
    if log_path:
        try:
            path = Path(log_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            file_handler_config = {
                "class": "logging.handlers.RotatingFileHandler",
                "level": level,
                "formatter": "standard",
                "filename": str(path),
                "maxBytes": 5 * 1024 * 1024,
                "backupCount": 3,
                "encoding": "utf-8",
            }
            handlers.append("file")
        except Exception as ex:
            # Defer file issues to console warnings
            logging.basicConfig(level=level)
            logging.getLogger(__name__).warning("Failed to prepare log file path %s: %s", log_path, ex)

    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": level,
                "formatter": "standard",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "uvicorn": {"level": level, "handlers": handlers, "propagate": False},
            "uvicorn.error": {"level": level, "handlers": handlers, "propagate": False},
            "uvicorn.access": {"level": level, "handlers": handlers, "propagate": False},
        },
        "root": {
            "level": level,
            "handlers": handlers,
        },
    }

    if file_handler_config:
        log_config["handlers"]["file"] = file_handler_config

    logging.config.dictConfig(log_config)
    logging.getLogger(__name__).info("Logging configured", extra={"log_path": log_path, "log_level": level})
