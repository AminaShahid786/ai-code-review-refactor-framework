"""FastAPI application entry point for the API Gateway.

Phase 4 (Backend Foundation) scope, exactly per the Implementation Roadmap:
an application factory, config loading, structured logging, CORS, generic
exception handling, and a single `/health` endpoint. No business routes,
authentication, database connections, or agent wiring exist yet — those
begin in Phase 5 onward.

Run locally with:
    uvicorn backend.gateway.main:app --host 0.0.0.0 --port 8000 --reload

Or via the containerized stack (Phase 4 addition to docker-compose.yml):
    make docker-up
"""

from __future__ import annotations

import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.gateway.config import Settings, get_settings
from backend.gateway.logging import configure_logging

logger = logging.getLogger(__name__)


def create_app(settings: Settings | None = None) -> FastAPI:
    """Application factory.

    Accepts an optional `Settings` override (used by tests) so the app can
    be constructed with test-specific configuration without touching real
    environment variables.
    """
    settings = settings or get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(
        title=settings.app_name,
        description=(
            "AI-Driven Code Review and Refactoring Framework — API Gateway. "
            "Multi-agent, SLM-based, RAG-augmented Python code review and "
            "refactoring platform."
        ),
        version="0.1.0",
        # Disable interactive docs in production; keep them in dev/test.
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
    )

    app.state.settings = settings

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _register_exception_handlers(app)
    _register_routes(app, settings)

    logger.info(
        "Gateway application created",
        extra={"environment": settings.environment, "app_name": settings.app_name},
    )
    return app


def _register_routes(app: FastAPI, settings: Settings) -> None:
    @app.get("/health", tags=["system"], summary="Liveness/health check")
    async def health() -> dict[str, str]:
        """Basic liveness probe.

        Returns 200 with a static status payload. This phase intentionally
        does not check downstream dependencies (database, cache, vector
        store, etc.) — those checks are added once the gateway actually
        connects to them, starting in later phases.
        """
        return {
            "status": "ok",
            "app_name": settings.app_name,
            "environment": settings.environment,
        }


def _register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        """Return a consistent JSON shape for expected HTTP errors (404, etc.)."""
        logger.warning(
            "HTTP exception",
            extra={"path": str(request.url), "status_code": exc.status_code, "detail": exc.detail},
        )
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """Return a consistent JSON shape for request validation failures."""
        logger.info(
            "Request validation failed",
            extra={"path": str(request.url), "errors": exc.errors()},
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.errors()},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Catch-all for anything unexpected — never leak internals to the client."""
        logger.exception(
            "Unhandled exception while processing request",
            extra={"path": str(request.url)},
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
        )


# Module-level app instance, used by `uvicorn backend.gateway.main:app`.
app = create_app()
