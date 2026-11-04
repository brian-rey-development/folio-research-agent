<p align="center">
  <img src="docs/brand/banner.png" alt="Folio. From filings to evidence." width="100%">
</p>

Folio is a market intelligence and investment research agent. It reads SEC filings and XBRL facts from EDGAR and returns a competitive map, a competitor matrix and an investment memo. Each claim cites an exact filing passage, and each number cites an exact XBRL fact. A separate eval suite measures retrieval, citation support, hallucination, latency and cost.

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
