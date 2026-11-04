# 0009 Eval fixtures and replay

This record has the status accepted. The learner and Claude accepted it on 2026-11-03 during the Folio design, and they revised it on 2026-11-04 when the product moved to SEC filings.

## Context

Folio reads live EDGAR sources, and their results change as new filings and amendments arrive. Live evals change a score with no code change, so no comparison between two pipeline versions in the case study stays valid.

## Decision

Each eval case records its tool responses and fetched documents as a fixture. An eval run replays the fixture, and the index filter limits retrieval to the filings in that fixture. A fixture changes only through a reviewed update, which records the date and the reason.

## Alternatives

A frozen snapshot of the full corpus is also reproducible, but it does not test the live discovery path. Live evals test everything, but their scores drift.

## Consequences

A score changes only when the code changes, so every comparison between pipeline versions is valid. The cost is storage for fixtures and a separate smoke test that checks the live clients still work.
