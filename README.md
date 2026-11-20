# idea-pipeline

A Claude plugin that turns any business-idea brief into **one researched top pick**. It works for consumer apps, B2B SaaS, traditional Indian industries adopting AI, or a new space. Every claim carries a source, and a dashboard fills in as each stage finishes.

- **Source hunter:** works out what to ask and names the exact sources to answer it (portals, associations, forums, review pages, job posts), not "industry reports".
- **Source checker:** builds its own list blind, then audits the hunter's plan for gaps and bias.
- **Researcher:** builds an evidence log. Each item has a URL, the date accessed, a quote and a confidence level.
- **Analyst:** scores ideas on the playbook's rubric and returns a top 10.
- **Red team:** the kill gate. It tries to sink every idea and leaves about three.
- **Entrepreneur:** picks one, says why, and names the riskiest assumption to test first.

You approve three things: the brief, the top 10 and the pick.

## How it works

```
Brief ──▶ [you approve] ──▶ Source hunter ⇄ Source checker (max 2 rounds)
      ──▶ Researcher (evidence log) ──▶ Analyst (top 10) ──▶ [you review]
      ──▶ Red team (≈3 survive) ──▶ Entrepreneur (one pick) ──▶ [you review] ──▶ registry
```

| Agent | What it does | What it can't do |
|---|---|---|
| **source-hunter** | Decomposes the brief, lists research questions and maps each to at least 3 independent source types with named URLs, vetted for credibility, recency, bias, access and India relevance. After research, it records which sources produced evidence and proposes playbook updates. | Research claims, score ideas |
| **source-checker** | Drafts its own source list before reading the plan, then diffs. It runs a coverage checklist (government, industry bodies, competitors and pricing, customer voice, demand signals, funding, academic, local-language) and a bias check, and returns PASS or a numbered gap list. | Edit the plan |
| **researcher** | Executes the plan and writes `evidence.json` | Make unsourced claims, score |
| **analyst** | Generates ideas from the evidence and scores them on the playbook rubric | Invent criteria or facts, browse |
| **red-team** | Checks that the rubric was followed, then tests willingness to pay, distribution, why now, incumbents, regulation and the playbook's kill criteria. Founder fit runs only if you add a profile. | Change scores |
| **entrepreneur** | Picks one idea and designs a test of 4 weeks or less with a success signal set in advance | Change scores or verdicts |

The `idea-pipeline` skill is the orchestrator. It's the only part that talks to you.

## Playbooks

A playbook tells every agent where to look, what signals matter, how to score and what kills an idea. The starter set is in [`playbooks/`](playbooks):

| Playbook | For | Scored on |
|---|---|---|
| [`b2c-apps`](playbooks/b2c-apps.md) | Consumer apps | Trends, revenue, willingness to pay, discoverability (ASO/SEO), retention, white space, rising apps |
| [`india-traditional-ai`](playbooks/india-traditional-ai.md) | AI for manufacturing, retail, construction, real estate, government in India | Pain and money at stake, who buys, sales cycle, integration effort, white space, why now (incl. UPI, ONDC, AA, ULI), newcomer success |
| [`b2b-saas`](playbooks/b2b-saas.md) | Software sold to businesses | Pain, ACV, buyer = user, sales cycle, switching cost, churn risk, white space, why now |

A brief can add a secondary playbook, such as B2B SaaS for Indian manufacturers. If no playbook fits, the orchestrator drafts one from [`_template.md`](playbooks/_template.md) and asks you to approve it once. It's then saved in your data folder for future runs. Playbooks are a starting point: the hunter always looks beyond them.

## Your data (private)

Everything from your runs lives in an **`idea-pipeline-data/`** folder in your working folder, not in this repo:

```
idea-pipeline-data/
├── registry.json          # index of past runs, so new runs reuse earlier research
├── playbooks/             # playbooks you approved or updated (override the plugin's)
├── founder_profile.md     # optional: only used for the red team's founder-fit check
└── runs/<yyyy-mm-dd>-<slug>/
    ├── brief.md  brief.json  market.json
    ├── source_plan.json  checker_list.json  source_check.json
    ├── evidence.json  top10.json  redteam.json  pick.json
    ├── source_yield.json  playbook_proposals.md
    └── dashboard.html
```

`idea-pipeline-data/` is in `.gitignore`.

## The dashboard

`dashboard.html` is a single self-contained page with no build step and no external requests. It is re-rendered after every stage, and sections that haven't run yet show as pending:

1. Brief in short
2. Target market
3. Sources, with links (and the checker's warning if gaps stayed open)
4. Top 10 ideas as short cards. Expand one for the reasoning, scores, red-team verdict and cited evidence.
5. The pick, why, and the riskiest assumption with its test

**Example:** open [`example-data/runs/2026-11-20-ai-indian-construction/dashboard.html`](example-data/runs/2026-11-20-ai-indian-construction/dashboard.html). It uses placeholder data labelled as an example, built from the brief in [`example-data/briefs/`](example-data/briefs/ai-indian-construction.md).

## Install

**Requirements:** Python 3.9+ (standard library only) and web search/fetch tools for the hunter, checker, researcher and red team. If your tools have different names, update the `tools:` lines in `agents/`.

**Claude Code:**
```
/plugin marketplace add unnatideep1/idea-pipeline
/plugin install idea-pipeline@idea-pipeline
```

**Cowork:** add `unnatideep1/idea-pipeline` as a plugin source in the plugins settings, then install **idea-pipeline**.

**Local clone:** `/plugin marketplace add /path/to/idea-pipeline`.

## Use

Say "Run the idea pipeline" with your idea in a sentence or a paragraph. Examples:

- "AI for Indian construction"
- "A B2C app for Indian college students preparing for placements"
- "B2B SaaS for Shopify merchants selling in India"

From a clone of this repo you can also run the scripts directly:

```
python skills/render-dashboard/scripts/render_dashboard.py idea-pipeline-data/runs/<run>

python skills/idea-registry/scripts/registry.py add idea-pipeline-data/runs/<run>
python skills/idea-registry/scripts/registry.py search "construction billing" --evidence
```

## Principles

- **Specific sources, checked twice.** Named sources with URLs, at least 3 independent types per question, and an independent checker.
- **No unsourced claims.** Every score of 4 or 5 and every fact on the dashboard links to evidence.
- **Same rubric every time.** The red team rejects scoring that strays from the playbook.
- **Try to kill before you pick.**
- **Reuse.** The registry and the source-yield log make each run smarter than the last.
- **Phase 1 stops at the pick.** No landing pages, ads or outreach.

## Status

v0.1: phase 1 (idea identification). The dashboard renderer and registry are tested on the example data. A full research run hasn't been done yet. Test a real install in Claude Code and Cowork to confirm `${CLAUDE_PLUGIN_ROOT}` paths and agent skill preloading.

## License

MIT
