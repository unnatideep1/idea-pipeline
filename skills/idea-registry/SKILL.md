---
name: idea-registry
description: Index finished idea-pipeline runs and search them, so a new run can reuse prior research, evidence and productive sources instead of starting from scratch. Use at the start of a run (search) and at the end of a run (add).
---

# Idea registry

`DATA/registry.json` lists every finished run: title, space, playbook, keywords, top 10 names, the pick, its riskiest assumption, evidence count, productive sources and the run folder path. The evidence itself stays in each run folder.

## Search (start of a run, before writing the brief)

```
python "${CLAUDE_PLUGIN_ROOT}/skills/idea-registry/scripts/registry.py" search "<industry, use case, buyer>" \
  --registry DATA/registry.json [--playbook <name>] [--evidence]
```

`--evidence` prints matching evidence items (claim, URL, date accessed) from related runs.

How to reuse:
- **Source hunter:** put `productive_sources` from related runs first in the plan.
- **Researcher:** re-open reused evidence, update `accessed`, and drop anything that no longer holds. Older than 12 months on a fast-moving question = re-research.
- **Analyst:** past top-10 ideas can be candidates again, but are scored fresh.

## Add (end of a run)

```
python "${CLAUDE_PLUGIN_ROOT}/skills/idea-registry/scripts/registry.py" add DATA/runs/<run> --registry DATA/registry.json
```

Re-adding a run updates its entry.
