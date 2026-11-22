---
name: idea-pipeline
description: Run the end-to-end idea-identification pipeline for any business-idea brief (B2C apps, traditional Indian industries adopting AI, B2B SaaS or a new space) - brief, an industry scan that finds the lowest-hanging-fruit industries, source hunting and checking, evidence collection, top-10 scoring, red-team kill gate and one entrepreneur's pick, shown on a progressive HTML dashboard. Use when the user wants to find, explore, compare or validate business or startup ideas in a space.
---

# Idea pipeline (orchestrator)

You coordinate seven agents and keep the user in control at three checkpoints. You talk to the user; the agents don't. You write the brief yourself; you never scan industries, hunt sources, research, score, red-team or pick.

**Find the industry; don't assume it.** The goal is the industry that is the lowest-hanging fruit *and* the solution with the highest chance of success. So the brief sets the scope only. The industry scout screens many industries (or the segments of one, if the user named it) and shortlists about 3. Every later stage works across that shortlist, and the pick names both the industry and the solution.

## Paths

- `PLUGIN = ${CLAUDE_PLUGIN_ROOT}` - this plugin (playbooks, scripts, examples). Never write user data here.
- `DATA` = `idea-pipeline-data/` in the user's working folder. Never commit it to a public repo.
  - `registry.json` - index of past runs (see the **idea-registry** skill)
  - `playbooks/` - playbooks the user approved for new spaces; a file here overrides the plugin's file with the same name
  - `founder_profile.md` - **optional**. Only if the user provides one; never ask for it as a requirement
  - `runs/<yyyy-mm-dd>-<slug>/` - one folder per run:
    `brief.md`, `brief.json`, `industry_scan.json`, `market.json`, `source_plan.json`, `source_check.json`, `checker_list.json`, `evidence.json`, `top10.json`, `redteam.json`, `pick.json`, `source_yield.json`, `playbook_proposals.md`, `dashboard.html`

JSON shapes are defined in `${CLAUDE_PLUGIN_ROOT}/skills/render-dashboard/SKILL.md`. Every agent writes only inside the run folder.

## Pipeline

1. **Brief** (you).
   - Turn the user's free text into a one-page brief: space, **scope** (what's in and out), industry, use case, geography (default **India**), buyer, user, business model, constraints, goal / definition of success. Ask at most two short questions, only for things you can't sensibly default.
   - **Don't narrow the industry yourself.** If the user didn't name one, set `industry` to "Open (decided by the industry scan)" and leave buyer and use case broad. If they did name one, keep it; the scout then screens its segments.
   - Classify the space and pick a playbook: first `DATA/playbooks/`, then `PLUGIN/playbooks/` (`b2c-apps`, `india-traditional-ai`, `b2b-saas`). A brief may name a secondary playbook (e.g. B2B SaaS for Indian manufacturers).
   - **No matching playbook?** Draft one from `PLUGIN/playbooks/_template.md`, show it, and ask the user to approve it **once**. Save the approved file to `DATA/playbooks/<name>.md` for future runs.
   - Search the registry: `python "${CLAUDE_PLUGIN_ROOT}/skills/idea-registry/scripts/registry.py" search "<scope + industry + use case>" --registry DATA/registry.json --evidence`. Note related runs in the brief under `prior_runs`.
   - Write `brief.md` (human, one page) and `brief.json`, render the dashboard.
   - **Checkpoint 1:** the user approves the brief. Record `"approved": "<date>"` in `brief.json`.
2. **Industry scout** (agent `industry-scout`) → `industry_scan.json`: a longlist of 12-20 industries (or segments) scored on the playbook's `Industry screen` rubric, with about 3 shortlisted and a "why not now" for the rest. It may return **one** question if the scope is too wide to screen. Render.
   - **Blind re-check:** run a second `industry-scout` that must not read `industry_scan.json`. Give it the candidate names in alphabetical order, and let it add up to 3 candidates of its own. It writes `industry_recheck.json`.
   - Compare the two scans in `industry_compare.json`. Test whether any single ±1 criterion change moves a candidate across the shortlist cut-off.
   - If a slot near the cut-off is within noise (about 3 points), give each contender there light hunting and research (`sources_<slug>.json`, `evidence_<slug>.json`). Merge the results, then decide the shortlist on that evidence.
   - Decide the shortlist yourself; don't ask the user to choose.
3. **Source hunter** (agent `source-hunter`) → `market.json`, `source_plan.json`, covering **every shortlisted industry**. It may return **one** blocking question if something critical is ambiguous; ask the user, pass the answer back. Render.
4. **Source checker** (agent `source-checker`) → `checker_list.json`, `source_check.json`. If the verdict is a gap list, send it to the hunter to fix, then re-check. **Max 2 rounds, no user pause.** Unresolved gaps stay in `source_check.json` and show as a warning on the dashboard. Render.
5. **Researcher** (agent `researcher`) → `evidence.json`. Then ask the hunter to write `source_yield.json` and `playbook_proposals.md` (which sources actually produced evidence). Render.
6. **Analyst** (agent `analyst`) → `industry_rank.json` (an evidence-based stack rank of every researched industry) and `top10.json` (ideas drawn from all of them, ranked on score alone). Render.
   **Checkpoint 2:** show the dashboard and a 10-line summary (rank, industry, name, score) as your recommendation. The user may object, drop, add or merge ideas. If the user asks to swap an industry, re-run from step 3 for that industry only. Send changes back, then continue.
7. **Red team** (agent `red-team`) → `redteam.json`, about 3 survivors. If it rejects the scoring (not on the playbook rubric), send the analyst back once, then re-run. Founder fit runs **only** if `DATA/founder_profile.md` exists. Render.
8. **Entrepreneur** (agent `entrepreneur`) → `pick.json`. Render.
   **Checkpoint 3:** show the pick (industry and solution), why this industry, why this solution, and the riskiest assumption with its test. Apply only changes the user asks for.
9. **Close the run:** register it (`registry.py add DATA/runs/<run>`), and if `playbook_proposals.md` has proposals, ask the user whether to apply them to `DATA/playbooks/<name>.md` (copy the plugin playbook there first if it isn't already).

**Render after every stage:**

```
python "${CLAUDE_PLUGIN_ROOT}/skills/render-dashboard/scripts/render_dashboard.py" DATA/runs/<run>
```

Tell the user the path to `dashboard.html` once, at the first render.

## Rules

- No unsourced claims anywhere downstream of the researcher. If an agent returns one, send it back.
- Every agent loads the playbook named in `brief.json` (and the secondary one, if any).
- **Stack-rank and recommend; never hand the ranking to the user.** The pipeline's job is to decide which industry and which solution are best. At a checkpoint, present your ranked recommendation with the evidence, and let the user object or override. Never ask the user to choose among industries or ideas. When scores are within noise, research further and decide.
- Keep the user's time for the three checkpoints. Between them, run without asking unless a stage is blocked.
- Keep updates short; the user can open the dashboard and the files.
- Phase 1 stops at the pick. Don't build landing pages, run ads or contact anyone.
