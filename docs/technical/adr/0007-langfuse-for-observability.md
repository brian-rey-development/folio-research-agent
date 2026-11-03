# 0007 Langfuse for observability

This record has the status accepted, and the learner and Claude accepted it on 2026-11-03 during the Folio design.

## Context

The exit condition requires visible latency and cost for each run. The failure analysis also needs the full path of a run, from the plan to each tool call and each model call.

## Decision

Langfuse records one trace for each run, with a span for each stage, tool call and model call. Eval scores go to Langfuse datasets and link to their traces. Development uses the Langfuse cloud free tier, so the local stack stays small.

## Alternatives

Logfire has native Pydantic AI traces and SQL over spans, but its LangGraph support comes through OpenTelemetry only. Arize Phoenix has strong RAG eval views, but Langfuse combines traces, prompt versions, datasets and scores in one place.

## Consequences

One tool answers what happened in a run, what it cost and how it scored. Langfuse accepts OpenTelemetry, so a later move to another backend keeps the instrumentation.
