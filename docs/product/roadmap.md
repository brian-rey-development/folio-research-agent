# Folio roadmap

The roadmap has six fixed stages, one for each week from November 3 to December 14, 2026. The learner has about 20 hours each week, so the full plan has a budget of about 120 hours.

Each stage has theory, experiments, an implementation and a measurable deliverable, and its learning module lives in `docs/learn/stage-N`. Each stage also names one part that the learner writes by hand. Sonnet agents build the scaffolding, the tests and the rest of the stage.

## Stages

| Week | Stage | Pipeline build | Product features | Learner builds by hand |
|---|---|---|---|---|
| 1, Nov 3 to 9 | LLM fundamentals and tool calling | A 2-hour spike on the 10-Ks of 5 cybersecurity companies, then a search agent on the EDGAR submissions and Company Facts APIs, filing metadata and a basic source-linked answer | Chat shell, projects, first deploy with a daily cost cap, Langfuse tracing | A raw tool-calling loop on the vendor SDK, before the Pydantic AI version |
| 2, Nov 10 to 16 | Retrieval and RAG | Full-text ingestion, 10-K and 10-Q section parsing, XBRL fact ingestion, chunking, embeddings, BM25, fixtures | Citation inspector, first 15 annotated eval cases | Hybrid search with RRF fusion, plus recall@k and nDCG |
| 3, Nov 17 to 23 | Context engineering | Reranking, evidence selection, provenance, token budgets, typed extraction of competitors, metrics and risks, with a cited sentence for each competitor edge | Competitor matrix, amendment and restatement flags | The context builder with a token budget and citation mapping |
| 4, Nov 24 to 30 | Agent orchestration | Controlled planning, multiple tool calls, persisted state, retries, bounded parallel filing analysis, verify stage | Research answer and investment memo artifacts, project memory with accept or reject, holdings list | The LangGraph graph with parallel fan-out and a bounded verify loop |
| 5, Dec 1 to 7 | Evaluation | Benchmark of at least 50 annotated cases, citation support scoring, failure modes, pipeline comparisons, cost and latency | Sector report artifact, investment style | The judge calibration and the failure taxonomy |
| 6, Dec 8 to 14 | Production engineering | Observability review, retries, caching, hardening | Competitive map view, Markdown export, case study with failure analysis, optional daily price source, buffer | The map graph schema and its validator |

The week 1 spike confirms two facts before any pipeline code depends on them. It checks that Item 1 separates cleanly from the rest of each 10-K, and it checks that XBRL has the metrics that the cases need. It also settles the open items in [the evaluation document](../technical/evaluation.md).

## Why the features are spread out

AI writes the scaffolding, the tests and most of the interface quickly, so the build column is not the bottleneck of this plan. The bottleneck is the learner's own time for the hand-written part of each stage, the financial literacy track, the reading, the annotation of eval cases and the review of AI-written code. For that reason the six weeks stay fixed, and the product features move to the week in which their inputs first exist. The citation inspector needs chunk positions and fact IDs from week 2, the competitor matrix needs the metric and risk records from week 3, and the artifacts need the verify stage from week 4. The investment memo reads the holdings in week 4 and gets its style from the investment style in week 5.

Deploying in week 1 turns the riskiest item into a weekly habit, where before it sat at the end of the plan with no time left to fix a failure. The cost of this order is that features arrive before the evaluation can measure them, which the verify stage in week 4 and the full benchmark in week 5 repair before the case study is written.

## Financial literacy track

The learner is not a finance expert, so a second track teaches financial literacy and statistics. These skills are necessary to judge whether the agent is right.

| Week | Topics |
|---|---|
| 1 | How to read a 10-K, and the three financial statements |
| 2 | BM25 and cosine similarity from first principles, and rank fusion |
| 3 | Margins, growth, cash flow and unit economics |
| 4 | Competitive strategy with Porter's five forces and Helmer's 7 Powers |
| 5 | Cohen's kappa and bootstrap confidence intervals |
| 6 | How to write a failure analysis |

## Baseline comparisons

Each stage compares a simple baseline with a more complex approach, because measured comparisons show engineering judgment. Examples are hybrid search against BM25 alone, reranking against no reranking, and parallel filing analysis against a sequential workflow. Each comparison becomes a section of the case study.

## Checkpoints

Every Sunday a checkpoint compares the pipeline and product columns of the week with the work that is done, and the deploy must stay live and inside its cost cap at every checkpoint. Week 6 holds only polish, so the optional price source and the interactive competitive map view are the cut line. If any earlier week slips, the price source goes first, then the interactive map view, then investment style. The typed competitor edges stay, because the matrix needs them, and the case study never moves.

## Learning materials

The core books are AI Engineering by Chip Huyen, Evals for AI Engineers, AI Agents in Action and Building Reliable AI Systems. For financial literacy, the start points are The Interpretation of Financial Statements by Benjamin Graham, and 7 Powers by Hamilton Helmer for competitive strategy. For the competitor gold labels, the Hoberg and Phillips work on text-based network industries explains how TNIC is built. Each stage module points to the chapters that support it.
