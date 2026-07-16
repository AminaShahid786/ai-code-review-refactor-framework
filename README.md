# AI-Driven Code Review and Refactoring Framework for Python

A production-grade, multi-agent AI system that reviews Python code, detects bugs and code
smells, generates behavior-preserving refactoring suggestions, validates every suggestion in
an isolated sandbox, explains its reasoning, and learns from user feedback over time.

The system is built entirely around locally-deployed **Small Language Models (SLMs)** —
no cloud LLM API is used anywhere in the review or refactoring path.

**Technology stack (per the FYP report's Tools and Technologies table — binding, not a
default):** Python/FastAPI backend; **plain HTML, CSS, and vanilla JavaScript frontend**
(no React/Vue/Angular, no build step, no npm dependency). See the architecture document's
§14 Technology Stack for the full list.

## Project Origin

This repository implements the Final Year Project **"AI-Driven Code Review and Refactoring
Framework for Python"** (National University of Modern Languages, Department of Computer
Science), extended from the original academic proposal into a full production architecture.

- Amina Shahid — BSCS-RC-504
- Azka Fazal — BSCS-RC-490
- Shafia Zahid — BSCS-RC-465
- Supervised by: Imran Javed

## Status

This repository is under active phased development. See `docs/` (added in a later phase) and
the project's Implementation Roadmap for the full phase-by-phase build plan.

**Completed phases:**

| Phase | Name | Status |
|---|---|---|
| 1 | Project Initialization & Repository Structure | ✅ Done |
| 2 | Development Environment & Tooling | ✅ Done |
| 3 | Docker & Container Infrastructure | ✅ Done |
| 4 | Backend Foundation (FastAPI) | ✅ Done |

**Current phase: Phase 4 — Backend Foundation.**
A running FastAPI gateway now exists (`backend/gateway/`), serving a single `/health`
endpoint, with structured JSON logging, CORS, and centralized exception handling. It does not
yet connect to any database, cache, or vector store, and has no business routes, auth, or
agents — those begin in Phase 5 onward.

## Getting Started

### 1. Clone and bootstrap the dev environment (Phase 2)

```bash
git clone <this-repo-url>
cd ai-code-review-framework
make setup
source .venv/bin/activate
```

This creates a Python virtual environment, installs development tooling (Ruff, Black, Mypy,
pre-commit, pytest), installs the git pre-commit hook, and creates your local `.env` from
`.env.example`.

### 2. Start the data layer (Phase 3)

```bash
make docker-up
make docker-ps
```

This brings up four containers on an internal Docker network (`ai-review-network`):

| Service | Purpose | Default local port(s) |
|---|---|---|
| PostgreSQL | Relational data store | `5432` |
| Redis | Cache / task queue broker | `6379` |
| Qdrant | Vector database | `6333` (HTTP), `6334` (gRPC) |
| MinIO | S3-compatible object storage | `9000` (API), `9001` (console) |

No agent or SLM-server containers are defined yet — those are introduced starting Phase 7 and
Phase 15 respectively. See `docker/docker-compose.yml` for full configuration and
`docker/Dockerfile.agent` for the (currently stubbed) agent worker image definition.

Stop the stack with `make docker-down` (data persists) or `make docker-clean` (also deletes
local volume data — destructive, dev-only).

### 3. Start the API Gateway (Phase 4)

The gateway is now part of the same Docker Compose stack:

```bash
make docker-up
curl http://localhost:8000/health
# → {"status":"ok","app_name":"ai-code-review-framework","environment":"development"}
```

Or run it directly on the host (without Docker) for faster iteration during development:

```bash
source .venv/bin/activate
pip install -e "."          # installs FastAPI/Uvicorn/Pydantic Settings/python-json-logger
uvicorn backend.gateway.main:app --host 0.0.0.0 --port 8000 --reload
```

Interactive API docs are available at `http://localhost:8000/docs` while `ENVIRONMENT` is not
`production`. No business routes exist yet — only `/health` and the auto-generated `/docs`.

## Repository Structure

```
ai-code-review-framework/
├── backend/            # FastAPI application: gateway, orchestrator, 12 specialized agents
│   ├── gateway/         # main.py (app factory + /health), config.py, logging.py
│   ├── orchestrator/    # Agent dispatch / task-queue orchestration (Phase 7+)
│   ├── agents/           # One package per agent (intake, preprocessing, static_analysis,
│   │                     #   context_builder, embedding, vector_db, memory, slm_review,
│   │                     #   refactoring, validation, explanation, feedback_learning) — Phase 8+
│   ├── models/           # SQLAlchemy ORM models (Phase 5+)
│   ├── schemas/          # Pydantic request/response schemas (Phase 5+)
│   └── api/              # REST route definitions (empty until Phase 6+)
├── frontend/            # Plain HTML/CSS/vanilla JavaScript — no framework, no build step
│                        #   (pages/, css/, js/ — populated starting Phase 22)
├── ml/                  # Model-serving, embeddings, prompts, and distillation pipeline
│   ├── distillation/     # Teacher-generation, supervised fine-tuning, LoRA/QLoRA
│   ├── embeddings/       # Embedding model wrappers
│   ├── memory/           # Long-term memory retrieval helpers
│   └── prompts/          # Versioned prompt templates per agent
├── validation/          # The 12-gate validation engine and sandbox execution runner
│   ├── gates/
│   └── sandbox_runner/
├── testing/             # Unit, integration, and end-to-end tests
├── docker/              # docker-compose.yml (data layer + gateway service),
│                        #   Dockerfile.gateway (real, Phase 4), Dockerfile.agent (stub, Phase 7+)
├── scripts/             # Operational and developer scripts
├── configs/             # Environment/service configuration files
├── logs/                # Local log output (not committed)
└── utils/               # Shared utility code
```

## Architecture

The full production architecture (12-agent multi-agent design, RAG pipeline, memory system,
knowledge distillation pipeline, database schema, API design, deployment, and security
architecture) is documented separately and drives every phase of this build. No component in
this repository deviates from that architecture.

## License

See `LICENSE`.
