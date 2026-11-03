<p align="center">
  <img src="docs/brand/logo.svg" alt="Folio" width="280">
</p>

<p align="center"><strong>From literature to evidence.</strong></p>

Folio is a biomedical research agent that searches scientific literature, reads the papers and analyzes the evidence for a research question. Every claim in its answers cites an exact passage in a real publication, so a reader can check it. It produces research answers, evidence matrices, literature reviews, research briefs and scientific diagrams, and it measures its own reliability with a separate evaluation suite.

Folio is also a six-week learning project that runs from November 3 to December 14, 2026. It builds senior-level Applied AI Engineering skills through real implementations, experiments and evaluations.

## Pipeline

A question goes through a fixed chain of stages. Folio plans the search and fetches papers from PubMed, Europe PMC, OpenAlex and ClinicalTrials.gov. It then retrieves passages with hybrid search, extracts typed study records and writes atomic claims with citations. A verify stage checks each claim before Folio writes the artifact. An evaluation suite outside the agent replays recorded cases and scores retrieval, citation support, hallucination types, latency and cost.

## Stack

| Layer | Tools |
|---|---|
| Web | Next.js, TypeScript, Tailwind, React Flow |
| API | Python 3.14, FastAPI, Pydantic |
| Agents | LangGraph between stages, Pydantic AI inside each LLM step |
| Models | Claude, OpenAI and Gemini through direct APIs |
| Storage | PostgreSQL with pgvector and BM25 (ParadeDB), SQLAlchemy Core, Alembic |
| Observability | Langfuse |
| Tooling | uv, pnpm, just, ruff, ty, pytest, import-linter, Oxlint, TypeScript 7 |

## Repository

```text
apps/api          FastAPI service
apps/web          Next.js chat, citations and artifact viewer
packages/core     domain types and pure rules
packages/sources  scientific API clients and the JATS parser
packages/ai       retrieval, agents, workflow, prompts
packages/db       tables, migrations, repositories, search SQL
packages/evals    cases, fixtures, metrics, judge, runners
infra             local stack
docs              product, technical and learning docs
```

## Quick start

The commands below need uv, pnpm, just and Docker on the machine, and they work after the workspace scaffold is in place.

```bash
just setup     # install Python and web dependencies
just db-up     # start the local ParadeDB database
just check     # lint, types, import layers and tests
```

## Documentation

- [Product docs](docs/product) hold the PRD, the roadmap and the brand, which say what Folio does and why.
- [Technical docs](docs/technical) hold the architecture, the evaluation method and the ADRs, which say how Folio works.
- [Learning modules](docs/learn) hold one module for each of the six stages, with concepts, exercises and a quiz.
