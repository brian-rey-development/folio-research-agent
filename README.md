<p align="center">
  <img src="docs/brand/banner.png" alt="Folio. From literature to evidence." width="100%">
</p>

Folio is a biomedical research agent. It searches PubMed, Europe PMC, OpenAlex and ClinicalTrials.gov, reads the papers and writes answers in which each claim cites an exact source passage. A separate eval suite measures retrieval, citation support, hallucination, latency and cost. The build is in stage 1 of 6, from November 3 to December 14, 2026.

## Stack

| Layer | Tools |
|---|---|
| Agents | LangGraph, Pydantic AI, Claude, OpenAI, Gemini |
| API | Python 3.14, FastAPI, Pydantic |
| Storage | Postgres with pgvector and BM25 (ParadeDB), SQLAlchemy, Alembic |
| Web | Next.js, TypeScript 7, Tailwind |
| Tooling | uv, pnpm, just, ruff, ty, Oxlint, pytest, Langfuse |

## Quick start

```bash
just setup    # install dependencies
just db-up    # start Postgres
just check    # lint, types, layer rules, tests
```

## Docs

| Folder | Content |
|---|---|
| [Product](docs/product) | PRD, roadmap, brand |
| [Technical](docs/technical) | Architecture, evaluation, ADRs |
| [AGENTS.md](AGENTS.md) | Rules for coding agents |
