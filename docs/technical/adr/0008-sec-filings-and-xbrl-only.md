# 0008 SEC filings and XBRL only

This record has the status accepted. The learner and Claude accepted it on 2026-11-03 during the Folio design, and they revised it on 2026-11-04 when the product moved to SEC filings.

## Context

Exact citations need exact text with stable offsets, and exact numbers need a source that states each value, its unit and its period. SEC EDGAR publishes both. Filings come as HTML with inline XBRL, and the XBRL Company Facts and Company Concept APIs on data.sec.gov return typed facts. PDF parsing is not needed, because it loses structure, breaks tables and gives noisy text.

## Decision

Folio reads only SEC EDGAR. It parses the text of 10-K, 10-Q and 8-K filings into sections. The sections that matter are Item 1 Business, Item 1A Risk Factors, Item 7 MD&A and Item 8 Financial Statements. Numbers come from XBRL facts, and each fact has an ID that a citation can point to. The parser normalizes each section to plain text and records its version, so citation offsets stay valid. The clients send a descriptive User-Agent and stay under the EDGAR fair access limit of 10 requests per second.

## Alternatives

Earnings call transcripts add context, but they are paid and they have no fixed source passage. A third-party financial data API is simple, but it adds a vendor cost and a second source of numbers. Those numbers do not trace back to a filing. Prices and news widen the product beyond the frozen scope.

## Consequences

Citations point to exact, stable spans and to exact XBRL facts, so a number check compares values and not text. The cost is coverage, because the product reads US filers that file a 10-K and not foreign filers that file a 20-F. Some numbers also exist only in the text of a filing. Numeric drift is therefore a release gate for numbers that have an XBRL fact, and a measured target for the rest. The week 1 spike confirms how well the Company Facts data covers the metrics that the cases need.
