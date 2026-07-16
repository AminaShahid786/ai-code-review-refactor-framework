"""REST route definitions package.

Intentionally empty at this phase (Phase 4 — Backend Foundation). The single
route that exists so far — `GET /health` — is defined directly in
`backend.gateway.main` since it is a gateway-level liveness probe, not a
business-domain route.

Starting in Phase 6 (Authentication & Authorization), this package will
contain one router module per resource (e.g. `auth.py`, `projects.py`,
`reviews.py`, `suggestions.py`), each exporting an `APIRouter` that
`backend.gateway.main` includes via `app.include_router(...)`.
"""
