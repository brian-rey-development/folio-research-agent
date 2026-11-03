# Folio PRD

This is version 0.2 of the requirements, written on 2026-11-03, and its scope is frozen for the build window that ends on December 14, 2026. The product tagline is "From literature to evidence," and it states the promise that every claim ends at a source.

## Summary

Folio is a biomedical research agent that combines scientific search, retrieval, context engineering and controlled workflows to produce evidence-grounded answers and artifacts with measurable reliability.

Every scientific claim that Folio writes traces back to an exact passage in a real publication. This principle decides the product, the architecture and the evaluation.

## Problem

A researcher who meets an unfamiliar biomedical question spends hours to find papers, read them, compare results and track which source says what. General chat assistants answer fast, but they cite papers that do not exist, misquote sources and state weak evidence as fact. Folio closes that gap with answers that a reader can check claim by claim.

## Users

The primary users are independent researchers, biotech founders, R&D analysts and science-focused teams, and the list below gives the jobs that they need done.

- Understand an unfamiliar scientific topic in hours instead of days.
- Find the relevant publications and judge the quality of each study.
- Compare findings, methods, limitations and conflicting evidence across studies.
- Produce cited research artifacts that they can reuse, edit and share.
- Continue an investigation later without rebuilding its context.

A typical user is a biotech founder who checks the evidence for a therapeutic mechanism and produces a cited brief with explicit limitations for investors.

## Research steps

A typical question asks whether creatine improves cognitive performance, and whether the effect is different under sleep deprivation. For a question like this, Folio runs these nine steps in order.

1. Understand the task and identify population, intervention, outcomes and study types.
2. Plan the investigation and select sources, search strategies and tools.
3. Search and fetch evidence from PubMed, Europe PMC, OpenAlex and ClinicalTrials.gov.
4. Read abstracts and open full text, and keep metadata and source locations.
5. Retrieve passages with lexical search, embeddings, metadata filters and reranking.
6. Analyze evidence for study design, sample size, results, limitations and contradictions.
7. Write a grounded answer that separates established, preliminary and unresolved findings.
8. Verify that each citation exists and supports the specific claim it is attached to.
9. Produce artifacts such as evidence tables, research reports and scientific diagrams.

The same system answers questions about longevity, biological mechanisms, treatments, biomarkers and published clinical research. Its specialization is biomedical evidence retrieval, analysis, traceability and research workflows, so it does not compete with general chat assistants on every topic.

## Medical safety

For a personal medical question, Folio gives evidence-based educational information and says when a clinician needs to assess the person. It never presents a research synthesis as a diagnosis or a treatment prescription, and every answer shows the certainty of its evidence.

## Capabilities

| Capability | Committed behavior |
|---|---|
| Papers | Search, fetch, parse, index and cite real publications |
| Evidence | Extract findings, study details, limitations and conflicts |
| Medical questions | Answer from retrieved evidence with stated uncertainty and the safety boundary above |
| Tools | Scientific APIs, document retrieval, search and structured operations |
| Projects | Keep research questions, conversations, sources and artifacts together |
| Project memory | Keep accepted decisions, open questions and verified findings for each project |
| Style memory | Keep explicit preferences for explanation depth, writing style, citation format and artifact structure |
| Artifacts | Research answers, evidence matrices, literature reviews, research briefs and scientific diagrams |
| Verification | Validate citations, detect unsupported claims, show conflicts and state uncertainty |
| Retractions | Flag any retracted paper at import and wherever an artifact cites it |
| Multi-agent | Add specialist workflows only where an evaluation measures their value |
| Export | Markdown export with citations and a bibliography |

## Artifacts

Artifacts are versioned objects that belong to a project, and each one stores its cited spans and its revision history.

| Artifact | Purpose | Output |
|---|---|---|
| Research answer | Answer a biomedical question from published evidence | Cited explanation |
| Evidence matrix | Compare studies, methods, results and limitations | Structured table |
| Literature review | Synthesize research across publications | Editable document |
| Research brief | Summarize a scientific question or mechanism | Short report |
| Scientific diagram | Show mechanisms, pathways and relationships | Editable SVG and interactive graph |

A user who asks "Explain how mTOR regulates autophagy, with a diagram" gets a graph in which each relationship links to its supporting passages. A click on a relationship opens those passages, and weakly supported relationships carry a visible mark. The diagram starts with simple pathway graphs, and publication-quality export comes after the research pipeline is reliable.

## Memory

Memory has clear scopes, and the user can inspect, correct and delete each saved item.

- Conversation memory is the message history of a project, so it needs no separate store.
- Project memory holds decisions, open questions and verified findings. The agent proposes an item, and the item is saved only after the user accepts it.
- Style memory holds explicit user preferences. It changes wording and structure only, so it never overrides evidence, numbers or project instructions.
- Artifact memory is the revision history of each artifact, including user edits.

## Primary workflow

1. Create a project with a research objective, a topic and optional style preferences for its artifacts.
2. Ask a research question, and let Folio search the sources, import new papers and analyze the evidence.
3. Inspect the source passage behind each claim, and compare the studies in the evidence matrix.
4. Generate an artifact such as a research brief, an evidence matrix or a scientific diagram.
5. Edit sections by hand, check the citations again and request targeted revisions from the agent.
6. Return later and continue with the project context, the artifacts and the preferences still in place.

## Interface

The first interface is a chat with visible citations and an artifact viewer. A citation inspector shows the exact source passage for each claim. Screen design gets no time in the first month, because the research system carries the value.

## Release criteria

The release on December 14, 2026 ships these items.

- Evidence-grounded answers to biomedical questions, with a citation inspector for each claim.
- Scientific search and retrieval over live sources, with full text where open access exists.
- Controlled multi-step research workflows with persisted state, retries and bounded parallel analysis.
- Projects with saved research context, accepted project memory and explicit style preferences.
- Research answers, research briefs, evidence matrices and source-backed scientific diagrams.
- An evaluation suite with at least 50 annotated cases, plus observability for latency and cost.
- A deployed demo with invite-only access and daily cost caps.
- A technical case study with a failure analysis.

The quality targets live in [the evaluation document](../technical/evaluation.md). The two hard gates are zero fabricated sources and zero misquotes in tested outputs.

## Success metrics

| Area | Metrics |
|---|---|
| AI quality | Retrieval recall, citation support, numeric accuracy, unsupported claim rate, correct abstention |
| Engineering | End-to-end latency, cost per completed workflow, tool failure recovery, test coverage |
| Product | Research tasks completed, artifacts generated, citation inspections, repeat project use |
| Portfolio | Public demo, documented architecture, benchmark results, evaluation dataset, case study |

Folio succeeds when a researcher moves from a scientific question to a reusable, evidence-grounded artifact and keeps the context to continue the investigation later.

## Exclusions

Collaborative editing, institutional SSO, billing, unrestricted autonomous browsing, fine-tuning and clinical decision support are out of scope. Longitudinal health memory, health conversation history and personalization belong to the separate Baseline project.

## Related documents

| Document | Content |
|---|---|
| [Roadmap](roadmap.md) | Six stages and the learning plan |
| [Brand](brand.md) | Visual identity |
| [Architecture](../technical/ARCHITECTURE.md) | System design |
| [Evaluation](../technical/evaluation.md) | Quality targets and test method |
