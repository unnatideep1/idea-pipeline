---
name: scan-industries
description: Screen many industries (or, if the brief names one industry, its sub-segments) for the lowest-hanging fruit before any deep research - score a longlist of 12-20 on the playbook's industry-screen rubric with sourced signals and shortlist about 3 for the rest of the idea-pipeline run. Use right after the brief is approved.
---

# Scan industries

The pipeline doesn't start from an industry and work backwards to a solution. It first asks **where** a new product is most likely to win, then **what** to build there. This step answers "where". The source hunter, researcher and analyst then work only on the shortlist, and the top 10 can span several industries.

Inputs: `RUN/brief.json`, the playbook(s) it names (section **Industry screen**), `DATA/registry.json`. Output: `RUN/industry_scan.json`.

## 1. Decide the level

- The brief leaves the industry open (`scope` is broad, `industry` is "Open"): screen **industries** (`level: "industry"`).
- The brief names one industry: screen its **segments** (sub-verticals, buyer types, regions or company sizes) instead (`level: "segment"`). The same rubric applies.

## 2. Build the longlist (12-20)

Start from the playbook's example list in **Industry screen**, then add from the brief's scope and from quick searches: sectors in recent government schemes, rules or rails; sectors with many job posts for manual back-office roles; sectors where newcomers raised money recently; past runs in the registry (`registry.py search`). Drop anything that breaks the brief's constraints and say so in `summary`.

Each candidate is something a founder could sell into: "MSME manufacturing (engineering & auto components)", not "manufacturing".

## 3. Score on the screen rubric

- Use **exactly** the criteria and weights in the playbook's `Industry screen` table. Score each 1-5. `score` = Σ(score × weight) / 5, rounded.
- This is a **screen**, not deep research: spend minutes per candidate, not hours. But a score of 4 or 5 still needs at least one signal with a URL you opened (a rule, a tender, a job post, a funding round, a complaint thread, a market figure). With no signal the score is at most 3.
- Check the playbook's **Kill criteria**: a candidate that hits one is not shortlisted, whatever its score; say which one.

## 4. Shortlist about 3

- Take the top scorers, usually 3 (2-4 is fine). Prefer a set that differs in buyer type, so one bad assumption doesn't sink all of them.
- Every shortlisted candidate gets `reason` ("why it's low-hanging fruit") and 2-4 `signals`.
- Every other candidate gets a one-sentence `reason` for "why not now". That's what a user reads when they ask "why not X?".

## 5. One question at most

If the brief's scope is so wide that the longlist is meaningless (e.g. "any business anywhere"), return **one** question to the orchestrator. Otherwise state your assumptions in `summary` and continue.

## Output

```json
{"level": "industry",
 "summary": "2-3 plain sentences: what scored highest and why",
 "rubric": [{"criterion": "Pain & money at stake", "weight": 20}],
 "candidates": [{"rank": 1, "name": "Construction & real estate",
   "one_liner": "who buys, what work is manual",
   "score": 81, "scores": {"Pain & money at stake": 5},
   "shortlisted": true, "reason": "why it's low-hanging fruit, or why not now",
   "signals": [{"text": "short fact", "url": "https://...", "source": "Publisher"}]}],
 "shortlist": ["Construction & real estate"]}
```

Write only `industry_scan.json`. Return a 3-line summary: how many screened, the shortlist with scores, anything killed.
