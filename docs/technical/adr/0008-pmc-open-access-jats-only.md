# 0008 PMC Open Access JATS only

This record has the status accepted, and the learner and Claude accepted it on 2026-11-03 during the Folio design.

## Context

Exact citations need exact text with stable offsets. PDF parsing loses structure, mixes columns, breaks tables and gives noisy text, and a good PDF pipeline takes about one week of work.

## Decision

Folio parses full text only from PMC Open Access JATS XML, which keeps sections, tables and references. Papers without open access full text use their abstract. The parser normalizes each section to plain text and records its version, so citation offsets stay valid.

## Alternatives

Docling or GROBID add PDF coverage, but the text is noisier and the work cost is high. Abstracts only is the simplest choice, but it loses methods, limitations and most numeric results.

## Consequences

Citations point to exact, stable spans. The cost is coverage, because only about 46% of GLP-1 randomized trials are open access, so the evals tag each case as full-text gold or abstract gold.
