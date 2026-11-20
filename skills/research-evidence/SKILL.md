---
name: research-evidence
description: Execute an idea-pipeline source plan and build the evidence log, where every claim has a source URL, date accessed, a verbatim quote or data point, and a confidence level. Use after the source plan has been checked.
---

# Research evidence

Inputs: `RUN/brief.json`, `RUN/market.json`, `RUN/source_plan.json`, `RUN/source_check.json`, the playbook(s), related past runs from the registry. Output: `RUN/evidence.json`, and updated size hints in `RUN/market.json`.

## Rules

- **No unsourced claims.** If you can't point to a page, it doesn't go in the log.
- One evidence item = one claim + one source. Two sources saying the same thing = two items (that's corroboration, which raises confidence).
- `quote` is verbatim text or the exact figure from the page (with units, year and geography). Don't paraphrase inside `quote`.
- `accessed` is today's date. Re-verify anything you reuse from a past run; update `accessed` or drop it.
- Prefer primary sources. If a number comes from a news article citing a report, find the report.

## Confidence

| Level | When |
|---|---|
| high | Primary or official source, recent, or two independent sources agree |
| medium | Credible secondary source, or one primary source that is older or indirect |
| low | Single forum/social post, vendor claim, estimate, or extrapolation |

## Process

1. Work question by question through `source_plan.json`. Aim for at least 3 items per question, from different source types.
2. Collect **idea seeds** as you go: complaints, workarounds (spreadsheets, WhatsApp, paper), regulations that create recurring work, new rails or mandates, newcomers growing fast. Log each as evidence; the analyst turns them into ideas.
3. Note sources that turned out dry, paywalled or off-topic in `notes` on the item or in a top-level `dry_sources` list; the hunter uses this for `source_yield.json`.
4. Replace `market.json` size hints with sourced figures where you found them, and add their evidence ids to the segment.

## Output

`evidence.json`:

```json
{"items": [{"id": "E01", "claim": "...", "source_id": "S03", "url": "https://...",
  "accessed": "2026-11-20", "quote": "...", "confidence": "high",
  "questions": ["Q2"], "notes": ""}],
 "dry_sources": [{"source_id": "S07", "reason": "paywalled"}]}
```

Ids are stable (`E01`, `E02`, ...); downstream agents cite them.
