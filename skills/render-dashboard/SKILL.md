---
name: render-dashboard
description: Render an idea-pipeline run folder into one self-contained, progressive dashboard.html (brief, industry scan, target market, sources, top 10, pick), and define the JSON files each stage writes. Use after every pipeline stage, or when the user asks to see a run.
---

# Render the dashboard

```
python "${CLAUDE_PLUGIN_ROOT}/skills/render-dashboard/scripts/render_dashboard.py" DATA/runs/<run> [--out path.html]
```

Python 3.9+, standard library only. Writes `dashboard.html` into the run folder: one file, no build step, no external assets, works offline, light and dark mode, responsive, semantic HTML. Missing files show as **Pending**, so render after every stage and the page fills in.

| # | Section | Reads | Pending until |
|---|---|---|---|
| 1 | Brief | `brief.json` | brief written |
| 2 | Industry scan (shortlist + "why not now" table) | `industry_scan.json` | industry scout done |
| 3 | Target market | `market.json` | source hunter done |
| 4 | Sources (+ checker warning) | `source_plan.json`, `source_check.json` | source hunter done |
| 5 | Top 10 ideas (+ industry tag, red-team badges) | `top10.json`, `redteam.json`, `evidence.json` | analyst done |
| 6 | The pick (industry + solution) | `pick.json` | entrepreneur done |

Citations (`E01`...) resolve to the evidence log, so the cards show the claim, quote, link and date. If `brief.json` has `"example": true`, an example banner is shown.

## File shapes

Only the fields shown are read by the renderer; agents may add more.

**brief.json**
```json
{"title": "", "slug": "", "summary": "", "space": "", "playbook": "", "secondary_playbook": "",
 "scope": "", "industry": "Open (decided by the industry scan)", "use_case": "", "geography": "India", "buyer": "", "user": "",
 "business_model": "", "constraints": [""], "goal": "", "prior_runs": [""], "approved": "yyyy-mm-dd"}
```

**industry_scan.json**
```json
{"level": "industry|segment", "summary": "", "rubric": [{"criterion": "", "weight": 20}],
 "candidates": [{"rank": 1, "name": "", "one_liner": "", "score": 0, "scores": {"criterion": 1},
   "shortlisted": true, "reason": "", "signals": [{"text": "", "url": "", "source": ""}]}],
 "shortlist": [""]}
```

**market.json**
```json
{"summary": "", "buyer": "", "user": "", "geography": "", "stage": "", "notes": "",
 "segments": [{"name": "", "industry": "", "size_hint": "", "description": "", "evidence": ["E01"]}]}
```

**source_plan.json**
```json
{"playbook": "", "shortlist": [""], "questions": [{"id": "Q1", "question": ""}],
 "sources": [{"id": "S01", "name": "", "url": "", "type": "", "industries": [""], "questions": ["Q1"], "why": "",
   "credibility": 5, "recency": "", "bias": "", "access": "free", "india_relevance": "high"}],
 "gaps": [""], "changes": [""]}
```

**source_check.json**
```json
{"verdict": "PASS|GAPS", "rounds": 2, "gaps": [""], "resolved": [""], "unresolved_gaps": [""]}
```

**evidence.json**
```json
{"items": [{"id": "E01", "claim": "", "source_id": "S01", "url": "", "accessed": "yyyy-mm-dd",
  "quote": "", "confidence": "high|medium|low", "questions": ["Q1"]}]}
```

**top10.json**
```json
{"playbook": "", "rubric": [{"criterion": "", "weight": 20}], "industries": [""],
 "ideas": [{"rank": 1, "id": "I01", "industry": "", "name": "", "one_liner": "", "score": 0,
   "scores": {"criterion": 1}, "why": "", "risks": [""], "evidence": ["E01"]}]}
```

**redteam.json**
```json
{"rubric_check": "PASS", "founder_fit_checked": false, "survivors": ["I01"],
 "verdicts": [{"idea_id": "I01", "outcome": "survive|killed", "reason": "",
   "attacks": [{"test": "", "finding": "", "evidence": ["E01"]}]}]}
```

**pick.json**
```json
{"idea_id": "I01", "industry": "", "name": "", "one_liner": "", "why_industry": "", "why": "", "evidence": ["E01"],
 "why_not_others": [{"name": "", "reason": ""}], "riskiest_assumption": "",
 "test": {"method": "", "success_signal": "", "cost": "", "duration": ""}}
```

See `${CLAUDE_PLUGIN_ROOT}/example-data/runs/2026-11-20-ai-traditional-indian-industries/` for a complete example.
