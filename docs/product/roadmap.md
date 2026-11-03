# Folio roadmap

The roadmap has six fixed stages, one for each week from November 3 to December 14, 2026. The learner has about 20 hours each week, so the full plan has a budget of about 120 hours.

Each stage has theory, experiments, an implementation and a measurable deliverable, and its learning module lives in `docs/learn/stage-N`. Each stage also names one part that the learner writes by hand. Sonnet agents build the scaffolding, the tests and the rest of the stage.

## Stages

| Week | Stage | Pipeline build | Product features | Learner builds by hand |
|---|---|---|---|---|
| 1, Nov 3 to 9 | LLM fundamentals and tool calling | Search agent on PubMed and OpenAlex, metadata and abstracts, a basic source-linked answer | Chat shell, projects, first deploy with a daily cost cap, Langfuse tracing | A raw tool-calling loop on the vendor SDK, before the Pydantic AI version |
| 2, Nov 10 to 16 | Retrieval and RAG | Full-text ingestion, JATS parsing, chunking, embeddings, BM25, fixtures | Citation inspector, first 15 annotated eval cases | Hybrid search with RRF fusion, plus recall@k and nDCG |
| 3, Nov 17 to 23 | Context engineering | Reranking, evidence selection, provenance, token budgets, structured study extraction | Evidence matrix, retraction flags | The context builder with a token budget and citation mapping |
| 4, Nov 24 to 30 | Agent orchestration | Controlled planning, multiple tool calls, persisted state, retries, bounded parallel paper analysis, verify stage | Research answer and research brief artifacts, project memory with accept or reject | The LangGraph graph with parallel fan-out and a bounded verify loop |
| 5, Dec 1 to 7 | Evaluation | Benchmark of at least 50 annotated cases, citation support scoring, failure modes, pipeline comparisons, cost and latency | Literature review artifact, style memory | The judge calibration and the failure taxonomy |
| 6, Dec 8 to 14 | Production engineering | Observability review, retries, caching, hardening | Scientific diagrams, Markdown export, case study with failure analysis, buffer | The diagram graph schema and its validator |

## Why the features are spread out

AI writes the scaffolding, the tests and most of the interface quickly, so the build column is not the bottleneck of this plan. The bottleneck is the learner's own time for the hand-written part of each stage, the evidence track, the reading, the annotation of eval cases and the review of AI-written code. For that reason the six weeks stay fixed, and the product features move to the week in which their inputs first exist. The citation inspector needs chunk positions from week 2, the evidence matrix needs the study records from week 3, and the artifacts need the verify stage from week 4.

Deploying in week 1 turns the riskiest item into a weekly habit, where before it sat at the end of the plan with no time left to fix a failure. The cost of this order is that features arrive before the evaluation can measure them, which the verify stage in week 4 and the full benchmark in week 5 repair before the case study is written.

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

Every Sunday a checkpoint compares the pipeline and product columns of the week with the work that is done, and the deploy must stay live and inside its cost cap at every checkpoint. Week 6 holds only polish, so scientific diagrams are the single cut line. If any earlier week slips, diagrams are dropped first, then style memory, and the case study never moves.

## Learning materials

The core books are AI Engineering by Chip Huyen, Evals for AI Engineers, AI Agents in Action and Building Reliable AI Systems. For evidence literacy, the start points are Testing Treatments by Evans and others, which is free online, and the Cochrane Handbook, chapters 8 and 14. Each stage module points to the chapters that support it.
