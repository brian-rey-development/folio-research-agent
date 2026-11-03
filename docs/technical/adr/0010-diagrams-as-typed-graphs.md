# 0010 Diagrams as typed graphs

This record has the status accepted, and the learner and Claude accepted it on 2026-11-03 during the Folio design.

## Context

A model that draws a scientific diagram freely can invent a relationship between two proteins, and no check can find it in an image. Folio promises that every claim traces to a source, and a diagram edge is a claim.

## Decision

The model outputs a typed graph of entities and relationships as a Pydantic model, and each relationship carries one or more cited spans. A validator rejects a relationship with no valid span, and the verify stage marks weakly supported edges. ELK.js computes the layout and React Flow renders the graph, so a click on an edge opens its source passages.

## Alternatives

Mermaid text from the model is fast, but it has no place for provenance on each edge. Image generation gives attractive output, but no check can verify its content.

## Consequences

Diagram evals score entity accuracy, relationship accuracy, citation support and completeness against a hand-checked graph. The cost is a custom renderer, so the first version shows simple pathway graphs only.
