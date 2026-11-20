---
name: score-ideas
description: Generate candidate business ideas from an idea-pipeline evidence log and score them on the playbook's rubric (trends, revenue opportunity, competition, white space, rising apps, newcomer success, need for change, plus space-specific criteria), producing a top 10 with reasoning and evidence ids for every claim. Use after research is complete.
---

# Score ideas

Inputs: `RUN/brief.json`, `RUN/industry_scan.json`, `RUN/market.json`, `RUN/evidence.json`, the playbook(s). Output: `RUN/top10.json`.

## 1. Generate candidates (15-30)

Turn evidence into ideas, from **every shortlisted industry** (at least 3 candidates each). Good sources of ideas:
- a painful manual workflow (paper, Excel, WhatsApp) with money or a deadline attached;
- a regulation or mandate that creates recurring work;
- a new rail, API or platform shift (UPI, ONDC, Account Aggregator, ULI, a new marketplace API) that makes something newly possible;
- incumbents' worst reviews, price hikes or ignored segments;
- a newcomer growing fast in a neighbouring segment or country.

Each candidate: an `industry` (one of the shortlist), a name (2-5 words), a one-liner (who it's for and what it does), and the evidence ids that motivate it. Drop ideas that break the brief's constraints.

## 2. Score on the playbook rubric

- Use **exactly** the criteria and weights in the playbook's `Scoring rubric`. If the brief names a secondary playbook, add its space-specific criteria as the playbook describes. Don't invent or reweight criteria; the red team rejects that.
- Score each criterion 1-5. Every score of 4 or 5 must be backed by at least one evidence id. With no evidence, the score is at most 2, and you say so.
- `score` = Σ(criterion score × weight) / 5, rounded (0-100).

## 3. Pick the top 10

Rank by score alone, across industries. Don't force a quota per industry; if one industry takes most of the top 10, that's a finding. Break ties on stronger evidence (more high-confidence items). Keep variety: if three ideas are near-duplicates, merge them.

For each idea write:
- `why`: 1-3 sentences in plain words. No hype, no "revolutionise".
- `risks`: 1-3 short bullets.
- `evidence`: the ids that support the claims in `why` and the high scores.

## Output

```json
{"playbook": "india-traditional-ai",
 "rubric": [{"criterion": "Pain & money at stake", "weight": 20}],
 "industries": ["Construction & real estate", "..."],
 "ideas": [{"rank": 1, "id": "I01", "industry": "Construction", "name": "...", "one_liner": "...", "score": 82,
   "scores": {"Pain & money at stake": 5}, "why": "...", "risks": ["..."], "evidence": ["E03", "E11"]}],
 "also_considered": [{"name": "...", "reason_dropped": "..."}]}
```
