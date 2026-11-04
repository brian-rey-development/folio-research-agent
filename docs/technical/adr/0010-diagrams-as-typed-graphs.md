# 0010 Diagrams as typed graphs

This record has the status accepted. The learner and Claude accepted it on 2026-11-03 during the Folio design, and they revised it on 2026-11-04 when the product moved to SEC filings.

## Context

A model that draws a competitive map freely can invent a rivalry between two companies, and no check can find it in an image. Folio promises that every claim traces to a source, and a map edge is a claim.

## Decision

The model outputs a typed graph of companies and relationships as a Pydantic model. Each edge (competes with, supplier of, customer of) carries one or more cited sentences from a filing. A validator rejects an edge with no valid sentence, and the verify stage marks weakly supported edges. ELK.js computes the layout and React Flow renders the graph, so a click on an edge opens its source sentence.

## Alternatives

Mermaid text from the model is fast, but it has no place for provenance on each edge. Image generation gives attractive output, but no check can verify its content.

## Consequences

Map evals score entity accuracy, relationship accuracy, citation support and completeness against a hand-checked graph. The cost is a custom renderer, so the first version shows simple graphs only.
