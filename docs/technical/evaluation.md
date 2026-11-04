# Folio evaluation

This document defines how Folio measures retrieval, grounding and hallucination. The evaluation system runs outside the agent and replays recorded cases, so a score changes only when the code changes.

## Fixtures

Folio reads live EDGAR sources, and live results change over time because new filings and amendments arrive. Each eval case therefore records its tool responses and fetched filings as a fixture, and an eval run replays that fixture. Live imports never enter eval retrieval, because an eval run filters the index by fixture membership. Replay also keeps the evaluation inside the EDGAR fair access limit of 10 requests per second. [ADR 0009](adr/0009-eval-fixtures-and-replay.md) explains this choice.

## Sector and case types

The evaluation starts with one sector, which is US-listed cybersecurity, and it covers 20 to 30 companies. Examples are CrowdStrike, Palo Alto Networks, Fortinet, Zscaler, SentinelOne and Okta. Check Point is a 20-F filer, so the set excludes it.

Cybersecurity is the first sector because almost every company in it claims leadership in some market. Those claims overlap and conflict, so the sector tests whether Folio detects a contradiction and attributes a claim to the company that makes it.

The 50 cases split into three case types, and each type tests a different skill.

| Case type | What it tests |
|---|---|
| Competitor discovery | Which companies a filing names as competitors, and how well Folio finds them |
| Exact numbers | Revenue, margin, cash flow and other figures taken from XBRL facts and from text |
| Conflicting claims | Overlapping leadership claims, contradiction detection and attribution to the speaker |

Each case has a tag for XBRL gold or text gold. A number that has an XBRL fact is an XBRL case, and a number that exists only in the text of a filing is a text case.

## Gold labels

The learner is not a finance expert, so the gold labels come from structured public sources and the learner checks them with a written protocol. This makes the labels defensible in the case study.

- XBRL facts give the gold for numbers, because a company tags each reported figure with a concept, a unit and a period.
- The competitors that each company names in its own Item 1 give one gold list for competitor discovery.
- The Hoberg and Phillips TNIC competitor pairs give a second gold list. TNIC is a text-based network industry classification that the authors compute from 10-K product descriptions.
- Every case has gold at the level of the filing, and one key claim in each case also has span gold.
- Each case has a question, gold filings, gold spans, an expected verdict (supports, refutes, or not enough evidence) and its source of truth.
- About 10 of the 50 cases have no answer in their fixture, so they test correct abstention. An example is the market share of a private company, which no filing states.

## Leakage control

A case whose competitor gold comes from the own Item 1 of a company removes that competition section from the fixture of that case. The agent then cannot copy the gold list, and it must find the competitors from other evidence such as peer filings and risk factors. TNIC is computed from the same kind of text, so the learner records which cases share a source and reports them as a group.

## Hallucination types

Hallucination splits into seven types, because one blended rate hides which control failed. The three deterministic checks are release gates, and the other measured targets appear in the case study with confidence intervals.

| Type | Failure | Control | Target |
|---|---|---|---|
| Fabricated source | Cites an accession number or fact ID that is not in the retrieved set | Pydantic validator against the retrieved ID set, one retry, then drop the claim | 0, gate |
| Misquote | Quoted text is not in the filing | Exact match against normalized section text at the cited offsets | 0, gate |
| Numeric drift | A value, unit or period differs from the source | Extract numbers from the claim and match them against the cited XBRL fact, or against the cited span when no fact exists | 0, gate for any number with an XBRL fact. 98% or more for numbers that exist only in text |
| Unsupported claim | A factual sentence has no citation | Split output into atomic claims, each needs one span or fact or more | 2% or less |
| Citation mismatch | The cited span does not support the claim | LLM judge, calibrated against human labels | 95% or more supported |
| Certainty inflation | Strong wording on weak evidence, such as a company self-claim of leadership stated as fact | Judge compares the wording with the evidence and checks that the claim names its speaker | 5% or less |
| Superseded or non-reliance filing | Cites a filing that a 10-K/A amended, or a filing under 8-K Item 4.02 non-reliance, without a flag | Check of the EDGAR submissions record for amendments and non-reliance items | 0 uncaught |

The structured output features differ between providers, so the fabricated source guarantee does not depend on an enum in a provider schema. The Pydantic validator is the guarantee, and it works the same for all providers.

## Other metrics

| Metric | Target |
|---|---|
| Retrieval recall@10, against gold passages present in the fixture | 80% or more |
| Competitor recall against the Item 1 gold and the TNIC gold | Reported, with a target set after the week 5 baseline |
| Correct abstention on cases with no answer | 90% or more |
| Competitive map edge and entity accuracy against a hand-checked graph | Reported |
| Latency and cost per completed run | Reported for each provider |

## Judge calibration

No public set matches this task exactly, so calibration relies mostly on hand labels. FinanceBench is a candidate public set for the citation support judge, and its fit is to be confirmed in week 5. If it does not fit, the learner labels 60 pairs of claim and passage by hand. The judge passes when Cohen's kappa against the human labels is 0.7 or more. No public set calibrates certainty inflation, so the learner labels 40 claims by hand for that judge, and many of them come from the leadership claims in Item 1. Any public set that calibrates or tests a part of the system does not count toward the 50 cases.

## To be confirmed by the week 1 spike

The week 1 spike fetches the 10-Ks of five cybersecurity companies. It settles the open items below before the case design is final.

| Item | What the spike checks |
|---|---|
| TNIC availability | Whether the TNIC data covers the chosen companies and fiscal years |
| Company Facts coverage | Whether XBRL has the metrics that the cases need for each chosen company |
| Item 1 separation | Whether the parser splits Item 1 cleanly from the rest of each 10-K |

## Statistics

With 50 cases, a single metric has a wide error range. Each reported metric therefore shows a bootstrap 95% confidence interval, and the case study claims no gain that sits inside that interval.
