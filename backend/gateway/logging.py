"""Structured logging configuration for the API Gateway.

Configures the root logger (and the Uvicorn loggers, so request/access logs
share the same format) to emit structured JSON lines via
`python-json-logger`. JSON logs are used from the very first phase so that
log aggregation (Loki/Grafana, introduced in Phase 26 — Monitoring &
Observability) requires no format migration later.
"""

from __future__ import annotations

import logging
import sys

from pythonjsonlogger import jsonlogger

_LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"

# Uvicorn's own loggers are configured alongside the root logger so that
# server startup/access logs match the rest of the application's format.
_UVICORN_LOGGER_NAMES = ("uvicorn", "uvicorn.error", "uvicorn.access")


def configure_logging(log_level: str = "INFO") -> None:
    """Configure structured JSON logging for the whole process.

    Idempotent: safe to call multiple times (e.g. once from `create_app()`
    and once from a test fixture) without duplicating log handlers.
    """
    resolved_level = getattr(logging, log_level.upper(), logging.INFO)

    formatter = jsonlogger.JsonFormatter(
        fmt=_LOG_FORMAT,
        rename_fields={"asctime": "timestamp", "levelname": "level", "name": "logger"},
    )

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(resolved_level)
    _replace_handlers(root_logger, handler)

    for logger_name in _UVICORN_LOGGER_NAMES:
        uvicorn_logger = logging.getLogger(logger_name)
        uvicorn_logger.setLevel(resolved_level)
        uvicorn_logger.propagate = False
        _replace_handlers(uvicorn_logger, handler)


def _replace_handlers(logger: logging.Logger, handler: logging.Handler) -> None:
    """Remove any existing handlers on `logger` and attach only `handler`.

    Prevents duplicate log lines if `configure_logging` is called more than
    once within the same process (e.g. in tests or hot-reload scenarios).
    """
    for existing in list(logger.handlers):
        logger.removeHandler(existing)
    logger.addHandler(handler)
