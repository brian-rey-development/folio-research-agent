# 0001 Record architecture decisions

This record has the status accepted, and the learner and Claude accepted it on 2026-11-03 during the Folio design.

## Context

Folio is a learning project, and the case study has to explain why each part has its current design. Decisions that live only in chat history get lost, and a reviewer cannot check them.

## Decision

Each decision that changes the structure, a dependency or a quality target gets an ADR in `docs/technical/adr`. An ADR has a number, a status, the context, the decision, the alternatives and the consequences, and it stays short. A new decision that replaces an old one gets a new ADR, and the old ADR changes its status to superseded.

## Consequences

The case study links to ADRs instead of repeating their reasons. Writing an ADR also forces a clear statement of the trade-off, which is a core skill of a senior engineer.
