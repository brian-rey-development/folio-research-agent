# Folio PRD

This is version 0.3 of the requirements, written on 2026-11-04, and its scope is frozen for the build window that ends on December 14, 2026. The product tagline is "From filings to evidence," and it states the promise that every claim and every number ends at a source.

## Summary

Folio is a market intelligence and investment research agent. It combines filing search, retrieval, context engineering and controlled workflows to produce evidence-grounded answers and artifacts with measurable reliability.

Every claim that Folio writes traces back to an exact passage in a filing, and every number traces back to an exact XBRL fact. This principle decides the product, the architecture and the evaluation.

## Problem

An analyst who meets an unfamiliar company or sector spends hours to find the right filings and read the business sections. The analyst then copies numbers into a sheet and tracks which source says what. General chat assistants answer fast, but they invent figures, misquote filings and repeat a company's own marketing as fact. Folio closes that gap with answers that a reader can check claim by claim and number by number.

## Users

The primary users are individual investors, equity analysts, founders and strategy teams that research competitors, and the list below gives the jobs that they need done.

- Understand an unfamiliar company or sector in hours instead of days.
- Find out who really competes with whom, according to what the companies themselves write.
- Compare companies with exact numbers and with the risks that each filing names.
- Produce cited artifacts that they can reuse, edit and share.
- Continue an investigation later without rebuilding its context.

A typical user is a founder who studies the competitors of a security vendor and writes a cited memo with explicit uncertainty for a partner.

## Product shape

The user gives a company or a sector, and Folio returns three outputs. The first is a competitive map that shows who competes with whom. The second is a competitor matrix that compares the companies with numbers and risks. The third is an investment memo that supports a decision, given the investment style and the current holdings of the user.

## Research steps

A typical question is "I am thinking about CrowdStrike. Who are its real competitors, how do they compare, and which risks matter if I already hold Palo Alto?" For a question like this, Folio runs these nine steps in order.

1. Read memory, which holds the style (growth), the horizon (five years) and the holdings (Palo Alto), and identify the company and the decision.
2. Plan the investigation and select the filings, the sections and the metrics.
3. Fetch the latest CrowdStrike 10-K from EDGAR and read the competitors that Item 1 names.
4. Fetch the 10-K of each named competitor, and keep accession numbers and section offsets.
5. Retrieve passages with lexical search, embeddings, metadata filters and reranking.
6. Take numbers from XBRL facts and risks from Item 1A, and mark claims that conflict.
7. Build the competitive map and the competitor matrix, then write the memo with its thesis, its risks and what would change the conclusion.
8. Verify each number against its XBRL fact and each quote as an exact text match.
9. Save the artifacts to the project with their cited spans and fact IDs.

The same system answers questions about a single company, a sector, a risk factor or a change between two fiscal years. Its specialization is filing retrieval, analysis, traceability and research workflows, so it does not compete with general chat assistants on every topic.

## Sources

Folio reads SEC EDGAR only. It uses the submissions API, EDGAR full-text search and the filing documents, which are 10-K, 10-Q and 8-K files in HTML and inline XBRL. It also uses the XBRL Company Facts and Company Concept APIs on data.sec.gov. EDGAR requires a descriptive User-Agent header and has a fair access limit of 10 requests per second.

The four 10-K sections that matter are Item 1 Business, which names competitors, Item 1A Risk Factors, Item 7 MD&A and Item 8 Financial Statements.

## Investment safety

Folio gives decision support with explicit uncertainty. It never says "buy" or "sell", and it never presents its output as personalized investment advice. It can relate findings to the holdings of the user. For example, it can note that a risk in one filing also applies to a company that the user holds. Every answer shows how strong its evidence is. A company statement such as "we are the leader" appears as an attributed claim and never as a fact.

## Capabilities

| Capability | Committed behavior |
|---|---|
| Filings | Search, fetch, parse, index and cite real SEC filings |
| Evidence | Extract competitors, metrics, segments, risks and conflicting claims |
| Company questions | Answer from retrieved filings with stated uncertainty and the safety boundary above |
| Tools | EDGAR APIs, document retrieval, search and structured operations |
| Projects | Keep research questions, conversations, sources and artifacts together |
| Project memory | Keep accepted theses, open questions and verified findings for each project |
| Investment style | Keep value or growth, horizon, risk tolerance, sectors to avoid and writing preferences |
| Holdings | Keep a list of held companies as context only |
| Artifacts | Research answers, competitor matrices, sector reports, investment memos and competitive maps |
| Verification | Validate quotes against text, validate numbers against XBRL, show conflicts and state uncertainty |
| Amendment flags | Flag a 10-K/A or a restatement at import and wherever an artifact cites it |
| Multi-agent | Add specialist workflows only where an evaluation measures their value |
| Export | Markdown export with citations and a source list |

## Artifacts

Artifacts are versioned objects that belong to a project, and each one stores its cited spans, its fact IDs and its revision history.

| Artifact | Purpose | Output |
|---|---|---|
| Research answer | Answer a question about a company or sector from filings | Cited explanation |
| Competitor matrix | Compare companies on metrics, segments and risks | Structured table |
| Sector report | Synthesize a sector across many companies | Editable document |
| Investment memo | Support a decision with a thesis, risks and what would change the conclusion | Short report |
| Competitive map | Show who competes with whom, and who supplies or buys from whom | Editable SVG and interactive graph |

A user who asks "Map the competitors of CrowdStrike" gets a typed graph. Each edge (competes with, supplier of, customer of) links to the sentence that supports it. A click on an edge opens that sentence in its filing, and weakly supported edges carry a visible mark. The map starts with simple graphs, and publication-quality export comes after the research pipeline is reliable.

## Memory

Memory has clear scopes, and the user can inspect, correct and delete each saved item.

- Conversation memory is the message history of a project, so it needs no separate store.
- Project memory holds theses, open questions and verified findings. The agent proposes an item, and the item is saved only after the user accepts it.
- Investment style holds the explicit preferences of the user, which are value or growth, horizon, risk tolerance, sectors to avoid and writing preferences. It changes emphasis, wording and structure only, so it never overrides evidence, numbers or project instructions.
- Holdings hold the companies that the user owns, for example "you hold these 8 companies". Folio uses them as context only.
- Artifact memory is the revision history of each artifact, including user edits.

## Primary workflow

1. Create a project with an objective, a company or sector, and optional style preferences.
2. Ask a question, and let Folio search EDGAR, import new filings and analyze the evidence.
3. Inspect the source passage behind each claim and the XBRL fact behind each number, and compare the companies in the competitor matrix.
4. Generate an artifact such as an investment memo, a competitor matrix or a competitive map.
5. Edit sections by hand, check the citations again and request targeted revisions from the agent.
6. Return later and continue with the project context, the artifacts and the preferences still in place.

## Interface

The first interface is a chat with visible citations and an artifact viewer. A citation inspector shows the exact filing passage or the XBRL fact for each claim. Screen design gets no time in the first month, because the research system carries the value.

## Release criteria

The release on December 14, 2026 ships these items.

- Evidence-grounded answers to questions about US-listed companies, with a citation inspector for each claim and number.
- Filing search and retrieval over live EDGAR sources, with section parsing and XBRL facts.
- Controlled multi-step research workflows with persisted state, retries and bounded parallel analysis.
- Projects with saved research context, accepted project memory, an investment style and a list of holdings.
- Research answers, investment memos, competitor matrices and source-backed competitive maps.
- An evaluation suite with at least 50 annotated cases, plus observability for latency and cost.
- A deployed demo with invite-only access and daily cost caps.
- A technical case study with a failure analysis.

The quality targets live in [the evaluation document](../technical/evaluation.md). The three hard gates are zero fabricated sources, zero misquotes and zero numeric drift on any number that has an XBRL fact.

## Success metrics

| Area | Metrics |
|---|---|
| AI quality | Competitor recall, citation support, numeric accuracy, unsupported claim rate, correct abstention |
| Engineering | End-to-end latency, cost per completed workflow, tool failure recovery, test coverage |
| Product | Research tasks completed, artifacts generated, citation inspections, repeat project use |
| Portfolio | Public demo, documented architecture, benchmark results, evaluation dataset, case study |

Folio succeeds when an analyst moves from a question about a company to a reusable, evidence-grounded artifact and keeps the context to continue the investigation later.

## Out of scope for v1

Market prices and valuation are out of scope. An optional single free daily price source can enter in week 6 only if time allows. It is the first item that the plan cuts. Portfolio analytics, news, earnings call transcripts (which are paid), non-US filers that file a 20-F, and trading are also out of scope.

Holdings are a list used as context only. Folio computes no returns and no portfolio risk, and this is an explicit non-goal.

Collaborative editing, institutional SSO, billing, unrestricted autonomous browsing, fine-tuning and personalized investment advice are out of scope too.

## Related documents

| Document | Content |
|---|---|
| [Roadmap](roadmap.md) | Six stages and the learning plan |
| [Brand](brand.md) | Visual identity |
| [Architecture](../technical/ARCHITECTURE.md) | System design |
| [Evaluation](../technical/evaluation.md) | Quality targets and test method |
