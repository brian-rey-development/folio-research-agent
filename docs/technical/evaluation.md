# Folio evaluation

This document defines how Folio measures retrieval, grounding and hallucination. The evaluation system runs outside the agent and replays recorded cases, so a score changes only when the code changes.

## Fixtures

Folio searches live sources, and live results change over time. Each eval case therefore records its tool responses and fetched documents as a fixture, and an eval run replays that fixture. Live imports never enter eval retrieval, because an eval run filters the index by fixture membership. [ADR 0009](adr/0009-eval-fixtures-and-replay.md) explains this choice.

## Seed topics

The cases start from three topics, and each topic tests a different skill.

| Topic | What it tests |
|---|---|
| Creatine and cognition | Small and conflicting trials, uncertainty and abstention |
| GLP-1 receptor agonists | Exact numbers from large trials and meta-analyses |
| mTOR and autophagy | Mechanisms, entity relationships and diagrams |

A Europe PMC query on 2026-11-03 for GLP-1 terms found 31,648 open access papers with full text. Only 1,430 of the 3,086 randomized trials are open access, so abstracts carry a large part of the evidence, and each case has a tag for full-text gold or abstract gold.

## Gold labels

The learner is not a biomedical expert, so the gold labels come from expert sources and the learner checks them with a written protocol. This makes the labels defensible in the case study.

- Published systematic reviews give the gold papers, because the studies that a review includes form an expert relevance set.
- Every case has paper-level gold, and one key claim in each case also has span-level gold.
- Each case has a question, gold papers, gold spans, an expected verdict (supports, refutes, or not enough evidence) and its source of truth.
- The source review of a case is removed from that case's fixture, so the agent cannot copy the pooled answer.
- About 10 of the 50 cases have no answer in their fixture, so they test correct abstention.

## Hallucination types

Hallucination splits into seven types, because one blended rate hides which control failed. The two deterministic types are release gates, and the other five are measured targets that the case study reports with confidence intervals.

| Type | Failure | Control | Target |
|---|---|---|---|
| Fabricated source | Cites an ID that is not in the retrieved set | Pydantic validator against the retrieved ID set, one retry, then drop the claim | 0, gate |
| Misquote | Quoted text is not in the source | Exact match against normalized section text at the cited offsets | 0, gate |
| Numeric drift | Effect size, n, p-value or CI differs from the source | Extract numbers from the claim and match them in the cited span | 98% or more |
| Unsupported claim | A factual sentence has no citation | Split output into atomic claims, each needs one span or more | 2% or less |
| Citation mismatch | The cited span does not support the claim | LLM judge, calibrated against human labels | 95% or more supported |
| Certainty inflation | Strong wording on weak evidence | Judge compares hedging with study design and population | 5% or less |
| Retracted source | Cites a retracted paper without a flag | Crossref Retraction Watch check | 0 uncaught |

The structured output features differ between providers, so the fabricated source guarantee does not depend on an enum in a provider schema. The Pydantic validator is the guarantee, and it works the same for all providers.

## Other metrics

| Metric | Target |
|---|---|
| Retrieval recall@10, against gold papers present in the fixture | 80% or more |
| Correct abstention on cases with no answer | 90% or more |
| Diagram entity and relationship accuracy against a hand-checked graph | Reported |
| Latency and cost per completed run | Reported for each provider |

## Judge calibration

SciFact gives claims with expert labels for support and refutation, so it calibrates the citation support judge. The judge passes when Cohen's kappa against the expert labels is 0.7 or more. No public set calibrates certainty inflation, so the learner labels 40 claims by hand for that judge. SciFact, PubMedQA and BioASQ calibrate and test parts of the system, but they do not count toward the 50 cases.

## Statistics

With 50 cases, a single metric has a wide error range. Each reported metric therefore shows a bootstrap 95% confidence interval, and the case study claims no gain that sits inside that interval.
