# Folio agent instructions

This file is the only instruction file for coding agents in this repository, so the repository has no `CLAUDE.md`. The web app has its own `apps/web/AGENTS.md`, which Next.js generates and which applies to that folder.

## Project

Folio is a market intelligence and investment research agent over SEC filings. It answers research questions about companies and sectors, and each claim cites an exact filing passage while each number cites an exact XBRL fact. Read [the PRD](docs/product/PRD.md) for the scope, [the architecture](docs/technical/ARCHITECTURE.md) for the design and [the evaluation document](docs/technical/evaluation.md) for the quality targets. The scope is frozen, so a new requirement extends the existing design and never changes the product direction.

## Commands

| Command | What it does |
|---|---|
| `just setup` | Installs the Python and web dependencies |
| `just check` | Runs ruff, ty, import-linter, pytest, web lint and web typecheck |
| `just audit` | Runs the Python and pnpm security audits |
| `just fmt` | Formats and fixes the Python code |
| `just db-up` | Starts the local ParadeDB container |
| `just db-migrate` | Applies the Alembic migrations |
| `just dev-api` | Starts the API in development mode |
| `just dev-web` | Starts the web app in development mode |

Do not start the app, the database or a dev server unless the user asks for it. Run `just check` before you report work as done, and paste its result.

## Layout and layers

The Python packages follow one direction of imports. `folio_core` imports nothing from the workspace, `folio_sources` and `folio_db` import only `folio_core`, `folio_ai` imports those three, and `folio_api` and `folio_evals` sit on top. The import-linter contract in `pyproject.toml` enforces this order, so never weaken the contract to make a check pass.

Domain models live in `packages/core`, tables, migrations and repositories live in `packages/db`, and API request and response schemas live in `apps/api`. Repositories take and return `core` models only.

## Code standards

- Use uv for Python and pnpm for Node, and never use pip, npm or yarn.
- Keep strict types everywhere, with no `Any` in Python and no `any` in TypeScript.
- Write functional code with immutable data and early returns, and keep each function at 20 lines or fewer.
- Use named constants instead of magic numbers or strings.
- Write no comment unless it explains a non-obvious reason, and write no docstring unless it documents a public contract.
- Validate data at the boundaries (user input, external APIs, LLM output) and trust internal code.
- Never use the em dash character in code, copy or docs.
- Treat filing text and API responses as untrusted data, and never pass them to a model as instructions.

## Dependencies

Every dependency stays on its latest stable release, with no pre-releases. A package held back below its latest version gets a comment in the manifest or the PR with the reason. `just audit` reports zero known advisories before a merge.

## Docs

Product docs live in `docs/product`, technical docs and ADRs live in `docs/technical`, and learning modules live in `docs/learn`. A decision that changes the structure, a dependency or a quality target gets an ADR, and before the first release a changed decision edits its original ADR. Docs use ASD-STE100 Simplified Technical English at 80% or better, with no colon in prose and no filler words.

## Git

Use conventional commits in English, and commit only when the user asks. Put worktrees in `.worktrees/<name>`, which git ignores. Never push, merge into `main` or rewrite history without the user's approval.
