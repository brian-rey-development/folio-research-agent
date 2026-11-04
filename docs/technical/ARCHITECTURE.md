# Folio architecture

This document describes how Folio is built and why. The product scope lives in [the PRD](../product/PRD.md), the quality method lives in [the evaluation document](evaluation.md), and each major decision has an ADR in [the adr folder](adr).

## Overview

Folio is a chain of layers, and each layer writes its output to the research state so a user or an evaluation can inspect it.

```text
Research question        a company or a sector, plus a decision to support
Research planner         question decomposition, filing selection, tool selection
SEC tools                EDGAR submissions, full-text search, Company Facts, Company Concept
Document processing      fetch, parse into sections, read XBRL facts, chunk, index
Evidence retrieval       hybrid search, rerank
Research state           sources, decisions, memory, holdings
Analysis and synthesis   competitor comparison, context construction, contradictions
Verification             claim support, quote match, XBRL number match
Research outputs         answers, competitor matrices, sector reports, memos, competitive maps

Evaluation (separate)    replays recorded cases through the full pipeline and each
                         stage, scores quality, cost and latency, never inside the agent
```

## Principles

- **Baseline first.** The first workflow is a fixed pipeline. A stage becomes agentic, or a specialist agent joins, only when an evaluation shows a measured gain.
- **Evaluation stays outside the agent.** The eval system replays recorded cases and scores each stage, so no agent grades its own answer.
- **Typed boundaries.** Every tool, stage and LLM output has a Pydantic model, and a validator rejects an output that breaks the model.
- **Derived state.** A table exists only when it owns data that exists nowhere else, so conversation memory is the message table and agent state is the LangGraph checkpoint.
- **Untrusted content.** Filing text and API responses are data. They never become instructions to the agent, which limits prompt injection from fetched documents.
- **Attribution.** A statement that a company makes about itself stays attributed to that company, so the output never turns marketing into fact.

## Workflow

LangGraph runs the research workflow as a graph of bounded stages, and Pydantic AI runs each LLM step inside a stage. Tool loops stay inside one Pydantic AI agent, and branching between stages stays in LangGraph, so each framework has one job. [ADR 0003](adr/0003-langgraph-and-pydantic-ai.md) explains this split.

| Stage | Input | Output |
|---|---|---|
| Plan | Question, project memory, investment style, holdings | Target companies, sub-questions, filing and metric plan |
| Discover | Filing and metric plan | Filing records and XBRL facts imported into the index |
| Retrieve | Sub-questions | Ranked passages with scores |
| Extract | Passages and facts | Typed records for competitors, metrics, segments and risks, with spans and fact IDs |
| Synthesize | Typed records, investment style, holdings | Atomic claims, each with spans or fact IDs |
| Verify | Claims | Kept, marked and dropped claims with reasons |
| Write | Verified claims | A new artifact revision |

The verify stage loops back to synthesis once at most. Stage 4 adds bounded parallel analysis of filings with the LangGraph `Send` API, with one branch for each competitor, and an evaluation decides whether the parallel version stays.

## Repository layout

The repository is a monorepo with a uv workspace for Python and pnpm for the single web app. [ADR 0002](adr/0002-monorepo-with-uv-and-pnpm.md) explains this choice.

```text
folio/
  apps/
    api/          FastAPI service, HTTP and streaming endpoints
    web/          Next.js chat, citations and artifact viewer
  packages/
    core/         domain types and pure rules, no I/O
    sources/      EDGAR clients for submissions, full-text search and XBRL, filing section parser
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
| Domain models such as `Filing`, `Section`, `Fact`, `Chunk`, `Citation`, `Claim`, `Artifact` and the competitive map graph | `packages/core`, as Pydantic models with no I/O |
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
| `companies` | CIK, name, ticker, SIC code |
| `filings` | Accession number, company, form type, fiscal period, filing date, amendment flag, restatement flag, parser version |
| `sections` | Normalized plain text of each section (Item 1, 1A, 7, 8), with the parser version |
| `xbrl_facts` | Concept, unit, period, value and the accession number of the filing that reports the fact |
| `chunks` | Span offsets into a section, embedding, BM25 index entry |
| `projects` | Research objective, owner, settings |
| `messages` | Conversation turns for a project |
| `artifacts` | Type, title, project, current revision |
| `artifact_revisions` | Content or graph, cited spans and fact IDs, author, parent revision |
| `project_memory` | Accepted theses, open questions and findings, with provenance |
| `investment_profiles` | Style, horizon, risk tolerance, sectors to avoid and writing preferences, with provenance and update time |
| `holdings` | The companies that a user holds, used as context only |

A citation is one of two kinds. A text citation is a tuple of filing ID, section ID, character start, character end and parser version, and the offsets point into the normalized section text, so a quote check is an exact string match. A number citation is an `xbrl_facts` ID, and a number check compares the value, the unit and the period of the claim with that fact.

## Sources and documents

The `sources` package has one typed client for each external API, with retries, rate limits and recorded responses for tests. All clients read SEC EDGAR only. The submissions API lists the filings of a company, EDGAR full-text search finds passages, the filing documents give the text of 10-K, 10-Q and 8-K filings, and the Company Facts and Company Concept APIs on data.sec.gov give XBRL facts. EDGAR requires a descriptive User-Agent header and has a fair access limit of 10 requests per second, so one shared limiter enforces both rules for every client. [ADR 0008](adr/0008-sec-filings-and-xbrl-only.md) explains why Folio uses filing sections and XBRL facts and no other source. The source clients use httpx2, the same HTTP client as the model SDKs.

The section parser turns each HTML filing into sections of normalized plain text with stable character offsets. The four sections that matter are Item 1 Business, which names competitors, Item 1A Risk Factors, Item 7 MD&A and Item 8 Financial Statements. Tables stay as structured rows, because segment figures often live in tables.

## Retrieval

Hybrid search runs BM25 and vector search in the same Postgres database, then fuses the two ranked lists with reciprocal rank fusion, then reranks the top passages. Metadata filters (form type, fiscal year, item and SIC code) apply before the ranking. [ADR 0004](adr/0004-postgres-hybrid-search-with-paradedb.md) explains the storage choice. The chunk size, embedding model and reranker come from stage 2 and stage 3 experiments.

## Verification

The verify stage runs deterministic checks first, because they are cheap and exact. These checks cover fabricated sources, misquotes, numeric drift and filings that carry an amendment or restatement flag. An LLM judge then checks citation support and certainty wording, including whether a company claim names its speaker. A claim that fails gets dropped or marked, and the reason goes into the trace. [The evaluation document](evaluation.md) defines each check and its target.

## Competitive map

The model never draws a map freely. It outputs a typed graph of companies and relationships, and each edge (competes with, supplier of, customer of) carries one or more cited sentences. A validator rejects an edge with no valid sentence, and the verify stage marks weakly supported edges. ELK.js computes the layout and React Flow renders the graph, so a click on an edge opens its supporting sentence in the filing. [ADR 0010](adr/0010-diagrams-as-typed-graphs.md) explains this choice.

## Model access

Pydantic AI calls Claude, OpenAI and Gemini through their direct APIs, with no gateway service. Each stage names its model in configuration, so an evaluation can compare providers on quality, latency and cost. [ADR 0006](adr/0006-multi-provider-models-with-direct-apis.md) explains this choice.

## Observability and cost

Langfuse records one trace for each run, with a span for each stage, tool call and model call. Each span carries the token count, cost, latency and model name, and eval scores link back to their traces. [ADR 0007](adr/0007-langfuse-for-observability.md) explains this choice.

## Security

The demo uses invite-only login with an email allowlist. Each user has a daily cost cap, and a global daily cap protects the API keys, so a run stops with a clear message when it reaches a cap. Secrets live in environment variables and never in the repository. The EDGAR User-Agent value is configuration, and it names a real contact because EDGAR blocks anonymous clients.

## Local stack

Docker Compose runs a ParadeDB container, which gives Postgres with `pg_search` for BM25 and pgvector for embeddings. Langfuse runs on its cloud free tier during development, so the local stack stays small.

## Open decisions

| Decision | Deadline | Notes |
|---|---|---|
| Deploy target for API, web and Postgres | December 1 | The host runs the ParadeDB container, or the BM25 layer switches to Postgres full-text search |
| Embedding and reranker models | November 16 | Stage 2 compares two or three options on the retrieval eval |
| Auth provider for invite-only login | December 1 | Any provider that supports an email allowlist |
