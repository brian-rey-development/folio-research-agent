# Folio roadmap

The roadmap has six fixed stages, one for each week from November 3 to December 14, 2026. The learner has about 20 hours each week, so the full plan has a budget of about 120 hours.

Each stage has theory, experiments, an implementation and a measurable deliverable, and its learning module lives in `docs/learn/stage-N`. Each stage also names one part that the learner writes by hand. Sonnet agents build the scaffolding, the tests and the rest of the stage.

## Stages

| Week | Stage | Build | Learner builds by hand |
|---|---|---|---|
| 1, Nov 3 to 9 | LLM fundamentals and tool calling | Search agent on PubMed and OpenAlex, metadata and abstracts, a basic source-linked answer, workspace and chat shell | A raw tool-calling loop on the vendor SDK, before the Pydantic AI version |
| 2, Nov 10 to 16 | Retrieval and RAG | Full-text ingestion, JATS parsing, chunking, embeddings, BM25, baseline eval set and fixtures | Hybrid search with RRF fusion, plus recall@k and nDCG |
| 3, Nov 17 to 23 | Context engineering | Reranking, evidence selection, provenance, token budgets, structured study extraction | The context builder with a token budget and citation mapping |
| 4, Nov 24 to 30 | Agent orchestration | Controlled planning, multiple tool calls, persisted state, retries, bounded parallel paper analysis | The LangGraph graph with parallel fan-out and a bounded verify loop |
| 5, Dec 1 to 7 | Evaluation | Research benchmark, citation support scoring, failure modes, pipeline comparisons, cost and latency | The judge calibration and the failure taxonomy |
| 6, Dec 8 to 14 | Production engineering | Reports, evidence tables, diagrams, saved context, deploy, observability, retries, caching, case study | The diagram graph schema and its validator |

## Evidence and math track

The learner is not a biomedical expert, so a second track teaches evidence literacy and statistics. These skills are necessary to judge whether the agent is right.

| Week | Topics |
|---|---|
| 1 | PICO, the evidence hierarchy, and how to read a randomized controlled trial |
| 2 | BM25 and cosine similarity from first principles, and rank fusion |
| 3 | Effect sizes, confidence intervals and p-values |
| 4 | Study design, bias and the GRADE certainty scale |
| 5 | Cohen's kappa and bootstrap confidence intervals |
| 6 | How to write a failure analysis |

## Baseline comparisons

Each stage compares a simple baseline with a more complex approach, because measured comparisons show engineering judgment. Examples are hybrid search against BM25 alone, reranking against no reranking, and parallel paper analysis against a sequential workflow. Each comparison becomes a section of the case study.

## Checkpoints

Every Sunday a checkpoint compares the build column of the week with the work that is done. Week 6 holds the most work, so its items ship in a fixed order. The deploy with cost caps comes first, then the case study, then reports and evidence tables, then saved context, then diagrams.

## Learning materials

The core books are AI Engineering by Chip Huyen, Evals for AI Engineers, AI Agents in Action and Building Reliable AI Systems. For evidence literacy, the start points are Testing Treatments by Evans and others, which is free online, and the Cochrane Handbook, chapters 8 and 14. Each stage module points to the chapters that support it.
