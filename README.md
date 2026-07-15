# AI-Driven Code Review and Refactoring Framework for Python

A production-grade, multi-agent AI system that reviews Python code, detects bugs and code
smells, generates behavior-preserving refactoring suggestions, validates every suggestion in
an isolated sandbox, explains its reasoning, and learns from user feedback over time.

The system is built entirely around locally-deployed **Small Language Models (SLMs)** —
no cloud LLM API is used anywhere in the review or refactoring path.

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

**Current phase: Phase 1 — Project Initialization & Repository Structure.**
No application logic, dependencies, or Docker services have been implemented yet — this phase
establishes only the canonical repository layout that every subsequent phase builds on.

## Repository Structure

```
ai-code-review-framework/
├── backend/            # FastAPI application: gateway, orchestrator, 12 specialized agents
│   ├── gateway/         # API entrypoint, config, auth
│   ├── orchestrator/    # Agent dispatch / task-queue orchestration
│   ├── agents/           # One package per agent (intake, preprocessing, static_analysis,
│   │                     #   context_builder, embedding, vector_db, memory, slm_review,
│   │                     #   refactoring, validation, explanation, feedback_learning)
│   ├── models/           # SQLAlchemy ORM models
│   ├── schemas/          # Pydantic request/response schemas
│   └── api/              # REST route definitions
├── frontend/            # React frontend application
├── ml/                  # Model-serving, embeddings, prompts, and distillation pipeline
│   ├── distillation/     # Teacher-generation, supervised fine-tuning, LoRA/QLoRA
│   ├── embeddings/       # Embedding model wrappers
│   ├── memory/           # Long-term memory retrieval helpers
│   └── prompts/          # Versioned prompt templates per agent
├── validation/          # The 12-gate validation engine and sandbox execution runner
│   ├── gates/
│   └── sandbox_runner/
├── testing/             # Unit, integration, and end-to-end tests
├── docker/              # Dockerfiles and docker-compose definitions
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
