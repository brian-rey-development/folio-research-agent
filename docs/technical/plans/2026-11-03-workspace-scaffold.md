# Scaffold plan

> Sonnet subagents run this plan task by task, and each step uses the checkbox (`- [ ]`) syntax so the progress stays visible.

**Goal.** Create the Folio monorepo with an SVG logo, a uv workspace, a pnpm web app, a local database and one command for all checks.

**Architecture.** A uv workspace holds five Python packages and the API app, and import-linter enforces the layer direction from the design. A pnpm workspace holds the single Next.js app, and Docker Compose runs ParadeDB for local hybrid search.

**Tech stack.** Python 3.14, uv, ruff, ty, pytest, import-linter, FastAPI, Next.js 16, Tailwind 4, pnpm, just, ParadeDB.

**Spec.** `docs/technical/ARCHITECTURE.md` and `docs/product/brand.md`

## Global constraints

- Python packages use the `src` layout and the import names `folio_core`, `folio_sources`, `folio_ai`, `folio_db`, `folio_evals` and `folio_api`.
- The layer order is `folio_api` and `folio_evals` on top, then `folio_ai`, then `folio_sources` and `folio_db`, then `folio_core`.
- Brand tokens are Forest `#0F3D33`, Teal `#146B5B`, Mint `#B7D6CC`, Sand `#EDECE7` and Ink `#1F2933`, with Inter as the only typeface.
- No em dash in any file, and all prose docs pass `ste_check.py` at 80% or more.
- No commit happens unless the user asks.

## Review focus

- A package that imports an upper layer makes `just check` fail.
- `just check` fails on a ruff error, a ty error, a failed pytest test or a failed web lint.
- The logo renders on GitHub with no installed fonts, because the wordmark is outlined paths.
- A missing `.env` does not stop the checks, because no check needs a secret.

---

### T1 Workspace

**Files.** The task creates `pyproject.toml`, `.python-version`, `justfile`, `.gitignore`, `.editorconfig`, `.env.example`, `package.json`, `pnpm-workspace.yaml`.

- [ ] Write the root `pyproject.toml` with `[tool.uv.workspace] members = ["packages/*", "apps/api"]`, ruff rules, ty settings, pytest settings and import-linter layer contracts.
- [ ] Write the `justfile` with the `setup`, `check`, `fmt`, `dev-api`, `dev-web`, `db-up` and `db-down` recipes.
- [ ] Run `uv sync`, and the expected result is a lock file with no errors.

### T2 Packages

**Files.** The task creates `packages/{core,sources,ai,db,evals}/pyproject.toml`, `src/folio_<name>/__init__.py`, `src/folio_<name>/py.typed` and `tests/test_import.py`.

- [ ] Write one import test for each package that asserts the package name.
- [ ] Run `uv run pytest`, and the expected result is 5 passed tests.
- [ ] Run `uv run lint-imports`, and the expected result is all contracts kept.

### T3 API

**Files.** The task creates `apps/api/pyproject.toml`, `apps/api/src/folio_api/main.py`, `apps/api/tests/test_health.py`.

- [ ] Write `test_health_returns_ok`, which asserts `GET /health` gives status 200 and `{"status": "ok"}`.
- [ ] Implement `create_app() -> FastAPI` in `main.py` with the `/health` route.
- [ ] Run `uv run pytest apps/api`, and the expected result is a pass.

### T4 Web

**Files.** The task creates `apps/web` with `create-next-app` (TypeScript, Tailwind, App Router, `src` folder), then change `src/app/globals.css`, `src/app/layout.tsx` and `src/app/page.tsx`.

- [ ] Put the five brand colors in the Tailwind theme, and load Inter with `next/font/google`.
- [ ] Replace the starter page with a Folio shell that shows the logo, the tagline and a disabled question box.
- [ ] Run `pnpm --filter web lint` and `pnpm --filter web build`, and the expected result is no errors.

### T5 Database

**Files.** The task creates `infra/compose.yaml`, `infra/initdb/001-extensions.sql`.

- [ ] Write a compose file with one `paradedb` service on port 5432 and a health check.
- [ ] Write the init SQL that creates the `vector` and `pg_search` extensions.
- [ ] Run `just db-up`, then query `pg_extension`, and the expected result lists both extensions.

### T6 Brand

**Files.** The task creates `docs/brand/logo.svg`, `docs/brand/mark.svg`, `docs/brand/icon.svg`, `README.md`, `AGENTS.md`.

- [ ] Draw the connected-block mark as one path, and outline the Inter Bold wordmark with fontTools.
- [ ] Check that the README quick start matches the `justfile` recipes, and change the README only where they differ.
- [ ] Run `just check`, and the expected result is all checks green.
