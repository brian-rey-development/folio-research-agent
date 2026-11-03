# 0006 Multi-provider models with direct APIs

This record has the status accepted, and the learner and Claude accepted it on 2026-11-03 during the Folio design.

## Context

A senior case study compares models on quality, latency and cost instead of picking one by habit. Folio also needs a fallback when one provider has an outage.

## Decision

Folio uses Claude, OpenAI and Gemini from day one, through their direct APIs and Pydantic AI. Each stage names its model in configuration, and the eval runner can run the full suite with each model. Langfuse records the cost for each call.

## Alternatives

A LiteLLM gateway adds budgets, fallbacks and caching, but it is one more service to run and debug. A single provider is simpler, but it gives no comparison data for the case study.

## Consequences

The eval suite produces a model comparison table with measured numbers. The cost is three API keys, three sets of rate limits and more eval runs, so the comparison runs on a schedule and not on every change.
