set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

setup:
    uv sync --all-packages
    if [ -f package.json ]; then pnpm install; fi

check:
    uv run ruff check .
    uv run ruff format --check .
    uv run ty check
    uv run lint-imports
    uv run pytest
    if [ -f apps/web/package.json ]; then pnpm --filter @folio/web lint; fi
    if [ -f apps/web/package.json ]; then pnpm --filter @folio/web typecheck; fi

fmt:
    uv run ruff format .
    uv run ruff check --fix .

db-up:
    docker compose -f infra/compose.yaml up -d

db-down:
    docker compose -f infra/compose.yaml down

db-migrate:
    cd packages/db && uv run alembic upgrade head

dev-api:
    uv run fastapi dev apps/api/src/folio_api/main.py

dev-web:
    pnpm --filter @folio/web dev
