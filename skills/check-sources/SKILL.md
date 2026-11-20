---
name: check-sources
description: Independently audit an idea-pipeline source plan - draft your own source list from the brief before reading the hunter's plan, diff the two, run a per-question coverage checklist and a bias check, and return PASS or a numbered gap list. Use after the source hunter writes source_plan.json.
---

# Check sources

You are independent. Your value comes from **not** being anchored by the hunter's plan.

Inputs: `RUN/brief.json`, `RUN/industry_scan.json`, `RUN/market.json`, the playbook(s). Then, and only then, `RUN/source_plan.json`. Outputs: `RUN/checker_list.json`, `RUN/source_check.json`.

## 1. Blind draft (before opening source_plan.json)

From the brief and playbook alone, list the research questions you'd ask and 2-3 named sources (with URLs) per question. Save as `checker_list.json` (`questions`, `sources`). Do this quickly; it's a reference, not a second plan.

## 2. Diff

Open `source_plan.json`. Note:
- sources you listed that the hunter missed and that would add a **new type or a stronger primary source** (not just more of the same);
- questions you asked that the hunter didn't.

## 3. Coverage checklist, per question and per shortlisted industry

Mark each type covered / missing / not applicable:

- Government / regulatory
- Industry bodies and reports
- Competitors and their pricing pages
- Customer voice: reviews, forums, social
- Demand signals: search trends, job posts
- Funding news / databases
- Academic
- Local-language sources (required when users work in Indian languages)

A question fails if it has fewer than **3 independent source types** for any shortlisted industry. Flag a plan that is lopsided (most sources serve one industry), since that quietly decides the winner before research.

## 4. Bias check

Flag the plan if:
- too global for an India brief (most sources low `india_relevance`);
- stale (key sources older than 3 years on a fast-moving question);
- paywalled-heavy (a question depends on sources the researcher can't open);
- single-type (one type carries most of the plan, e.g. all trade media);
- vendor-heavy (claims about market size come only from people selling into it);
- vague (any entry is a category, not a named source with a URL).

Spot-check at least five URLs; dead or off-topic links are gaps.

## 5. Verdict

Write `source_check.json`:

```json
{"verdict": "PASS" | "GAPS", "round": 1, "rounds": 1,
 "gaps": ["1. Q4 has no customer-voice source; add Play Store reviews for <app>", "..."],
 "resolved": [], "unresolved_gaps": [],
 "independent_list_size": 0, "overlap": 0}
```

Each gap is numbered, specific and fixable (name the source or type you expect). On round 2, move fixed items to `resolved` and anything still open to `unresolved_gaps`. After round 2, stop: the orchestrator continues and the dashboard shows `unresolved_gaps` as a warning.
