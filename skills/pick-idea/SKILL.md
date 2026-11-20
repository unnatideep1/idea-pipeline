---
name: pick-idea
description: Choose the single best idea from the red-team survivors of an idea-pipeline run, explain why in plain words with evidence, and name the riskiest assumption plus a cheap test to run first. Use after the red-team stage.
---

# Pick the idea

Think like a founder who has to spend the next two years on this. Choose one idea, which also chooses the industry. Explain both: why this industry is the lowest-hanging fruit (use `industry_scan.json` and the evidence) and why this solution has the best chance of success in it.

Inputs: `RUN/brief.json`, `RUN/industry_scan.json`, `RUN/evidence.json`, `RUN/top10.json`, `RUN/redteam.json`, the playbook(s). Output: `RUN/pick.json`.

## How to choose among survivors

Weigh, in this order:
1. **Clearest payer** - someone already spends money or staff time on the problem.
2. **Fastest path to 10 paying customers** given the brief's constraints.
3. **Strength of evidence** - more high-confidence, independent items.
4. **Room to grow** - the next product or segment after the wedge.

The highest score doesn't automatically win; say so if you pick a lower-ranked survivor, and why.

## Riskiest assumption

The one belief that, if false, kills the idea, and that the evidence doesn't already settle. Usually about willingness to pay, a buyer's process (approvals, compliance), or distribution. Then design a test that:
- runs in **≤4 weeks** for a small cost;
- uses the playbook's validation method where it fits (e.g. a landing page with paid sign-ups for B2C; paid pilots or LOIs for B2B);
- has a success signal set **before** the test (a number, not "positive feedback").

## Output

```json
{"idea_id": "I01", "industry": "...", "name": "...", "one_liner": "...",
 "why_industry": "2-3 plain sentences: why this industry first",
 "why": "3-5 plain sentences: why this solution", "evidence": ["E11", "E12"],
 "why_not_others": [{"name": "...", "reason": "..."}],
 "riskiest_assumption": "...",
 "test": {"method": "...", "success_signal": "...", "cost": "...", "duration": "..."}}
```
