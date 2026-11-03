# 0005 SQLAlchemy Core and Alembic

This record has the status accepted, and the learner and Claude accepted it on 2026-11-03 during the Folio design.

## Context

Folio needs versioned migrations, typed table definitions and special Postgres DDL for the `bm25` and `hnsw` indexes. The hybrid search SQL is a learning target, so no tool hides it.

## Decision

The `db` package uses SQLAlchemy 2.1 Core tables, Alembic migrations and psycopg 3. Migrations use autogenerate for plain columns and `op.execute` for the index DDL. Search queries are raw SQL in the `db` package. Repositories take and return `core` domain models, so table rows never leak into upper layers.

## Alternatives

Plain SQL files with dbmate or Atlas give the most direct SQL practice, but they have no autogenerate. SQLModel gives one class for the table and the Pydantic model, but it couples the domain shape to the table shape.

## Consequences

The stack is the most common one in Python job posts. The cost is two layers to learn, and the mapping between rows and domain models is code that the repositories own.
