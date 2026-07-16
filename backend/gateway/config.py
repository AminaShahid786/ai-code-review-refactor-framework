"""Application configuration for the API Gateway.

Settings are loaded from environment variables (and, for local development,
from a `.env` file at the repository root — see `.env.example`). Only
settings meaningful at this phase (Phase 4 — Backend Foundation) are defined
here. Later phases (database URLs in Phase 5, JWT secrets in Phase 6, etc.)
will extend this `Settings` class rather than introduce a parallel one.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Strongly-typed application settings, sourced from the environment.

    Field names are matched case-insensitively against environment variable
    names of the same name (Pydantic Settings default behaviour) — e.g.
    `app_name` reads from the `APP_NAME` environment variable, matching
    `.env.example`.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # --- General application settings (introduced in Phase 2's .env.example) ---
    app_name: str = "ai-code-review-framework"
    environment: str = "development"
    log_level: str = "INFO"

    # --- Gateway server settings (Phase 4) ---
    gateway_host: str = "0.0.0.0"  # noqa: S104
    gateway_port: int = 8000

    # --- CORS (Phase 4) ---
    # Comma-separated list of allowed origins. The frontend (Phase 22) is
    # plain HTML/CSS/vanilla JS with no build step — see .env.example for
    # the default local static-serving ports this assumes.
    cors_allowed_origins: str = "http://localhost:8080,http://localhost:5500"

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse the comma-separated CORS origins string into a clean list."""
        return [origin.strip() for origin in self.cors_allowed_origins.split(",") if origin.strip()]

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    """Return a cached, process-wide Settings instance.

    Cached with `lru_cache` so environment/`.env` parsing happens exactly
    once per process, and every part of the application shares the same
    configuration object.
    """
    return Settings()
