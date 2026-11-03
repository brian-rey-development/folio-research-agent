# Folio architecture

This document describes how Folio is built and why. The product scope lives in [the PRD](../product/PRD.md), the quality method lives in [the evaluation document](evaluation.md), and each major decision has an ADR in [the adr folder](adr).

## Overview

Folio is a chain of layers, and each layer writes its output to the research state so a user or an evaluation can inspect it.

```text
Research question        scientific, biomedical or medical
Research planner         question decomposition, search strategy, tool selection
Scientific tools         PubMed, Europe PMC, OpenAlex, ClinicalTrials.gov, Crossref
Document processing      fetch, parse, chunk, index
Evidence retrieval       hybrid search, rerank
Research state           sources, decisions, memory
Analysis and synthesis   study comparison, context construction, contradictions
Verification             claim support, citation validity
Research outputs         answers, reports, evidence tables, diagrams

Evaluation (separate)    replays recorded cases through the full pipeline and each
                         stage, scores quality, cost and latency, never inside the agent
```

## Principles

- **Baseline first.** The first workflow is a fixed pipeline. A stage becomes agentic, or a specialist agent joins, only when an evaluation shows a measured gain.
- **Evaluation stays outside the agent.** The eval system replays recorded cases and scores each stage, so no agent grades its own answer.
- **Typed boundaries.** Every tool, stage and LLM output has a Pydantic model, and a validator rejects an output that breaks the model.
- **Derived state.** A table exists only when it owns data that exists nowhere else, so conversation memory is the message table and agent state is the LangGraph checkpoint.
- **Untrusted content.** Paper text and API responses are data. They never become instructions to the agent, which limits prompt injection from fetched documents.

## Workflow

LangGraph runs the research workflow as a graph of bounded stages, and Pydantic AI runs each LLM step inside a stage. Tool loops stay inside one Pydantic AI agent, and branching between stages stays in LangGraph, so each framework has one job. [ADR 0003](adr/0003-langgraph-and-pydantic-ai.md) explains this split.

| Stage | Input | Output |
|---|---|---|
| Plan | Question, project memory | PICO fields, sub-questions, search plan |
| Discover | Search plan | Paper records imported into the index |
| Retrieve | Sub-questions | Ranked passages with scores |
| Extract | Passages | Typed study records with numbers and spans |
| Synthesize | Study records, style preferences | Atomic claims, each with spans |
| Verify | Claims | Kept, marked and dropped claims with reasons |
| Write | Verified claims | A new artifact revision |

The verify stage loops back to synthesis once at most. Stage 4 adds bounded parallel analysis of papers with the LangGraph `Send` API, and an evaluation decides whether the parallel version stays.

## Repository layout

The repository is a monorepo with a uv workspace for Python and pnpm for the single web app. [ADR 0002](adr/0002-monorepo-with-uv-and-pnpm.md) explains this choice.

```text
folio/
  apps/
    api/          FastAPI service, HTTP and streaming endpoints
    web/          Next.js chat, citations and artifact viewer
  packages/
    core/         domain types and pure rules, no I/O
    sources/      PubMed, Europe PMC, OpenAlex, ClinicalTrials.gov, Crossref clients, JATS parser
    ai/           retrieval, Pydantic AI agents, LangGraph workflow, prompts
    db/           tables, migrations, repositories, search SQL
    evals/        cases, fixtures, metrics, judge, runners
  infra/          Docker Compose now, infrastructure code later
  docs/
    product/      PRD, roadmap, brand
    technical/    architecture, evaluation, ADRs, plans
    learn/        stage modules
    case-study/   final write-up
```

The dependency direction goes one way. `core` imports nothing from the workspace, `sources` and `db` import `core`, `ai` imports all three, and `apps/api` and `evals` sit on top. An import-linter contract enforces this direction, so a wrong import fails the checks.

## Persistence

The database layer uses SQLAlchemy 2.1 Core tables, Alembic migrations and psycopg 3. Each kind of schema has one home, so a change in one layer does not leak into another. [ADR 0005](adr/0005-sqlalchemy-core-and-alembic.md) explains this choice.

| What | Where |
|---|---|
| Domain models such as `Paper`, `Chunk`, `Citation`, `Claim`, `Artifact` and the diagram graph | `packages/core`, as Pydantic models with no I/O |
| Table definitions | `packages/db/src/folio_db/tables.py` |
| Migrations | `packages/db/migrations`, with `op.execute` for the `bm25` and `hnsw` indexes |
| Repositories | `packages/db/src/folio_db/repositories`, which take and return `core` models only |
| Hybrid search SQL | `packages/db`, called by the retrieval code in `packages/ai` |
| Rank fusion and reranking | `packages/ai/retrieval`, as pure functions with unit tests |
| API request and response schemas | `apps/api/src/folio_api/schemas` |
| TypeScript types for the web | Generated from the FastAPI OpenAPI document |
| LangGraph checkpoint tables | The `langgraph` schema, owned by `langgraph-checkpoint-postgres`, and Alembic ignores it |

A repository interface (a Python `Protocol`) goes in `core` only when the `ai` layer needs a fake for its tests. The `infra` folder holds only the runtime setup.

## Data model

| Table | What it owns |
|---|---|
| `papers` | Identifiers (PMID, PMCID, DOI, NCT), metadata, license, retraction status |
| `sections` | Normalized plain text of each section, with the parser version |
| `chunks` | Span offsets into a section, embedding, BM25 index entry |
| `projects` | Research objective, owner, settings |
| `messages` | Conversation turns for a project |
| `artifacts` | Type, title, project, current revision |
| `artifact_revisions` | Content or graph, cited spans, author, parent revision |
| `project_memory` | Accepted decisions, open questions and findings, with provenance |
| `style_preferences` | Explicit user preferences, with provenance and update time |

A citation is a tuple of paper ID, section ID, character start, character end and parser version. The offsets point into the normalized section text, so a quote check is an exact string match.

## Sources and documents

The `sources` package has one typed client for each external API, with retries, rate limits and recorded responses for tests. PubMed and Europe PMC give search and abstracts, PMC Open Access gives full text as JATS XML, OpenAlex gives metadata and links, ClinicalTrials.gov gives trial registrations, and Crossref gives retraction data. [ADR 0008](adr/0008-pmc-open-access-jats-only.md) explains why Folio parses JATS XML and no PDFs. The source clients use httpx2, the same HTTP client as the model SDKs.

The JATS parser turns each article into sections of normalized plain text with stable character offsets. Tables stay as structured rows, because effect sizes often live in tables.

## Retrieval

Hybrid search runs BM25 and vector search in the same Postgres database, then fuses the two ranked lists with reciprocal rank fusion, then reranks the top passages. Metadata filters (study type, year, population) apply before the ranking. [ADR 0004](adr/0004-postgres-hybrid-search-with-paradedb.md) explains the storage choice. The chunk size, embedding model and reranker come from stage 2 and stage 3 experiments.

## Verification

The verify stage runs deterministic checks first, because they are cheap and exact. These checks cover fabricated sources, misquotes, numeric drift and retracted sources. An LLM judge then checks citation support and certainty wording. A claim that fails gets dropped or marked, and the reason goes into the trace. [The evaluation document](evaluation.md) defines each check and its target.

## Diagrams

The model never draws a diagram freely. It outputs a typed graph of entities and relationships in which each relationship carries one or more cited spans, and a validator rejects a relationship with no valid span. ELK.js computes the layout and React Flow renders the graph, so a click on an edge opens its supporting passages. [ADR 0010](adr/0010-diagrams-as-typed-graphs.md) explains this choice.

## Model access

Pydantic AI calls Claude, OpenAI and Gemini through their direct APIs, with no gateway service. Each stage names its model in configuration, so an evaluation can compare providers on quality, latency and cost. [ADR 0006](adr/0006-multi-provider-models-with-direct-apis.md) explains this choice.

## Observability and cost

Langfuse records one trace for each run, with a span for each stage, tool call and model call. Each span carries the token count, cost, latency and model name, and eval scores link back to their traces. [ADR 0007](adr/0007-langfuse-for-observability.md) explains this choice.

## Security

The demo uses invite-only login with an email allowlist. Each user has a daily cost cap, and a global daily cap protects the API keys, so a run stops with a clear message when it reaches a cap. Secrets live in environment variables and never in the repository.

## Local stack

Docker Compose runs a ParadeDB container, which gives Postgres with `pg_search` for BM25 and pgvector for embeddings. Langfuse runs on its cloud free tier during development, so the local stack stays small.

## Open decisions

| Decision | Deadline | Notes |
|---|---|---|
| Deploy target for API, web and Postgres | December 1 | The host runs the ParadeDB container, or the BM25 layer switches to Postgres full-text search |
| Embedding and reranker models | November 16 | Stage 2 compares two or three options on the retrieval eval |
| Auth provider for invite-only login | December 1 | Any provider that supports an email allowlist |
