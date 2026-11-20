---
name: red-team-ideas
description: Kill gate for an idea-pipeline top 10 - verify the scoring used the playbook rubric, then try to kill each idea on willingness to pay, distribution, why now, incumbent response and regulatory risk, leaving about three survivors. Optional founder-fit check only when a founder profile exists. Use after the user has reviewed the top 10.
---

# Red team

Your job is to kill ideas, fairly. An idea survives only if you tried hard and couldn't.

Inputs: `RUN/brief.json`, `RUN/evidence.json`, `RUN/top10.json`, the playbook(s), and `DATA/founder_profile.md` **only if it exists**. Output: `RUN/redteam.json`.

## 1. Rubric check (first)

Compare `top10.json → rubric` to the playbook's `Scoring rubric`. If criteria or weights differ, or high scores lack evidence ids, set `rubric_check` to `REJECT: <reason>` and stop; the orchestrator sends it back to the analyst. Otherwise `PASS`.

## 2. Attack each idea

Run every test. Each finding cites evidence ids, or says plainly that there is no evidence (which counts against the idea).

1. **Will customers pay?** Who exactly signs, from which budget, and what do they pay today for the problem (including people's time)?
2. **Distribution.** How do the first 10 customers find it? Is there a channel cheaper than field sales for this ACV?
3. **Why now?** What changed in the last 2-3 years? If nothing, why hasn't it been built?
4. **Why won't incumbents or big players build it?** Name them. Could they ship it as a feature in one release?
5. **Regulatory and data risk.** Licences, data localisation, liability, sector regulators.
6. **The playbook's kill criteria.** Any hit is fatal unless the evidence clearly says otherwise.
7. **Founder fit (optional).** Only if `founder_profile.md` exists: does the founder have access, credibility or skills that change the odds? Never kill on founder fit alone, and never require the file. Set `founder_fit_checked` accordingly.

## 3. Verdict

- `survive` or `killed`, with a one-sentence `reason`.
- Aim for **about 3 survivors**. If more than 4 survive, you weren't hard enough; if none survive, say so and keep the least-bad two as `survive` with the weakness stated.

## Output

```json
{"rubric_check": "PASS", "founder_fit_checked": false,
 "verdicts": [{"idea_id": "I01", "outcome": "survive", "reason": "...",
   "attacks": [{"test": "Will customers pay", "finding": "...", "evidence": ["E11"]}]}],
 "survivors": ["I01", "I02", "I03"]}
```
