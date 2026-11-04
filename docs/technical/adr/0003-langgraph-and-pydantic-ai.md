# 0003 LangGraph and Pydantic AI

This record has the status accepted. The learner and Claude accepted it on 2026-11-03 during the Folio design, and they revised it on 2026-11-04 when the product moved to SEC filings.

## Context

The research workflow has many stages, shared state, retries, a verify loop and parallel filing analysis. Each LLM step also needs typed output, tools and a model that can change for comparisons.

## Decision

LangGraph runs the workflow between stages, with its state, checkpoints, branches and parallel fan-out. Pydantic AI runs each LLM step inside a stage, with typed output, tools and the provider choice. Tool loops stay inside one Pydantic AI agent, and branching between stages stays in LangGraph.

## Alternatives

LangGraph alone gives one framework, but its LLM calls have weaker typing. Pydantic AI alone has a graph module, but it has less support for checkpoints and parallel fan-out. A raw SDK with a custom loop teaches the most, so stage 1 builds one by hand as a baseline before the framework version.

## Consequences

Each framework has one clear job, so a reader knows where to look for a given behavior. The cost is two abstractions to learn, and the boundary rule needs review in each pull request, because both frameworks can run a tool loop.
