---
name: idea-pipeline
description: Run the end-to-end idea-identification pipeline for any business-idea brief (B2C apps, traditional Indian industries adopting AI, B2B SaaS or a new space) - brief, source hunting and checking, evidence collection, top-10 scoring, red-team kill gate and one entrepreneur's pick, shown on a progressive HTML dashboard. Use when the user wants to find, explore, compare or validate business or startup ideas in a space.
---

# Idea pipeline (orchestrator)

You coordinate six agents and keep the user in control at three checkpoints. You talk to the user; the agents don't. You write the brief yourself; you never hunt sources, research, score, red-team or pick.

## Paths

- `PLUGIN = ${CLAUDE_PLUGIN_ROOT}` - this plugin (playbooks, scripts, examples). Never write user data here.
- `DATA` = `idea-pipeline-data/` in the user's working folder. Never commit it to a public repo.
  - `registry.json` - index of past runs (see the **idea-registry** skill)
  - `playbooks/` - playbooks the user approved for new spaces; a file here overrides the plugin's file with the same name
  - `founder_profile.md` - **optional**. Only if the user provides one; never ask for it as a requirement
  - `runs/<yyyy-mm-dd>-<slug>/` - one folder per run:
    `brief.md`, `brief.json`, `market.json`, `source_plan.json`, `source_check.json`, `checker_list.json`, `evidence.json`, `top10.json`, `redteam.json`, `pick.json`, `source_yield.json`, `playbook_proposals.md`, `dashboard.html`

JSON shapes are defined in `${CLAUDE_PLUGIN_ROOT}/skills/render-dashboard/SKILL.md`. Every agent writes only inside the run folder.

## Pipeline

1. **Brief** (you).
   - Turn the user's free text into a one-page brief: space, industry, use case, geography (default **India**), buyer, user, business model, constraints, goal / definition of success. Ask at most two short questions, only for things you can't sensibly default.
   - Classify the space and pick a playbook: first `DATA/playbooks/`, then `PLUGIN/playbooks/` (`b2c-apps`, `india-traditional-ai`, `b2b-saas`). A brief may name a secondary playbook (e.g. B2B SaaS for Indian manufacturers).
   - **No matching playbook?** Draft one from `PLUGIN/playbooks/_template.md`, show it, and ask the user to approve it **once**. Save the approved file to `DATA/playbooks/<name>.md` for future runs.
   - Search the registry: `python "${CLAUDE_PLUGIN_ROOT}/skills/idea-registry/scripts/registry.py" search "<industry + use case>" --registry DATA/registry.json --evidence`. Note related runs in the brief under `prior_runs`.
   - Write `brief.md` (human, one page) and `brief.json`, render the dashboard.
   - **Checkpoint 1:** the user approves the brief. Record `"approved": "<date>"` in `brief.json`.
2. **Source hunter** (agent `source-hunter`) → `market.json`, `source_plan.json`. It may return **one** blocking question if something critical is ambiguous; ask the user, pass the answer back. Render.
3. **Source checker** (agent `source-checker`) → `checker_list.json`, `source_check.json`. If the verdict is a gap list, send it to the hunter to fix, then re-check. **Max 2 rounds, no user pause.** Unresolved gaps stay in `source_check.json` and show as a warning on the dashboard. Render.
4. **Researcher** (agent `researcher`) → `evidence.json`. Then ask the hunter to write `source_yield.json` and `playbook_proposals.md` (which sources actually produced evidence). Render.
5. **Analyst** (agent `analyst`) → `top10.json`. Render.
   **Checkpoint 2:** show the dashboard and a 10-line summary (rank, name, score). The user may drop, add or merge ideas; send changes back to the analyst, then continue.
6. **Red team** (agent `red-team`) → `redteam.json`, about 3 survivors. If it rejects the scoring (not on the playbook rubric), send the analyst back once, then re-run. Founder fit runs **only** if `DATA/founder_profile.md` exists. Render.
7. **Entrepreneur** (agent `entrepreneur`) → `pick.json`. Render.
   **Checkpoint 3:** show the pick, why, and the riskiest assumption with its test. Apply only changes the user asks for.
8. **Close the run:** register it (`registry.py add DATA/runs/<run>`), and if `playbook_proposals.md` has proposals, ask the user whether to apply them to `DATA/playbooks/<name>.md` (copy the plugin playbook there first if it isn't already).

**Render after every stage:**

```
python "${CLAUDE_PLUGIN_ROOT}/skills/render-dashboard/scripts/render_dashboard.py" DATA/runs/<run>
```

Tell the user the path to `dashboard.html` once, at the first render.

## Rules

- No unsourced claims anywhere downstream of the researcher. If an agent returns one, send it back.
- Every agent loads the playbook named in `brief.json` (and the secondary one, if any).
- Keep the user's time for the three checkpoints. Between them, run without asking unless a stage is blocked.
- Keep updates short; the user can open the dashboard and the files.
- Phase 1 stops at the pick. Don't build landing pages, run ads or contact anyone.
