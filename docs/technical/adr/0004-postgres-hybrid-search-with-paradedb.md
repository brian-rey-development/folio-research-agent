# 0004 Postgres hybrid search with ParadeDB

This record has the status accepted, and the learner and Claude accepted it on 2026-11-03 during the Folio design.

## Context

Biomedical retrieval needs exact term matches for drug names, genes and outcomes, and it also needs semantic matches for paraphrased findings. The project data (papers, projects, artifacts) also needs a relational store.

## Decision

One PostgreSQL database holds the app data, the BM25 index and the vectors. Locally it runs the ParadeDB image, which has `pg_search` for true BM25 and pgvector for embeddings. Retrieval fuses the two ranked lists with reciprocal rank fusion, and the learner writes that fusion by hand in stage 2.

## Alternatives

Qdrant has native sparse and dense hybrid search, but it adds a second store to keep in sync. LanceDB has zero operations, but it is less common in production. Postgres full-text search with `ts_rank` is available on every managed Postgres, but it is close to BM25 and not equal to it.

## Consequences

One database means one backup, one transaction scope and SQL joins between search results and metadata. The cost is that many managed Postgres services do not offer `pg_search`. The deploy target therefore runs the ParadeDB container, or the lexical side switches to `ts_rank` and an eval measures the difference.
