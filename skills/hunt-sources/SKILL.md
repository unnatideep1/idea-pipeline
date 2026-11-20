---
name: hunt-sources
description: Decompose an approved idea brief into research questions and build a vetted source plan of named, specific sources (with URLs, credibility, access method and India relevance) for each question, plus the identified target market. Use when an idea-pipeline run needs its source plan, or to fix gaps raised by the source checker.
---

# Hunt sources

The quality of the whole run depends on this step. A generic plan ("industry reports", "news") is a failure. Every source must be something a researcher can open tomorrow.

Inputs: `RUN/brief.json`, the playbook(s) it names, `DATA/registry.json` (past runs). Outputs: `RUN/market.json`, `RUN/source_plan.json`. Later: `RUN/source_yield.json`, `RUN/playbook_proposals.md`.

## 1. Decompose the brief

Write down, for yourself: industry, segment (by size, region, sub-vertical), country and states/cities, buyer (who signs), user (who uses), business model, stage of the market (nascent / growing / mature / being disrupted).

- If something **critical** is ambiguous and the wrong guess would waste the run (e.g. "construction" = residential developers or government contractors?), return **one** question to the orchestrator and stop. Otherwise state your assumption in `market.json → notes` and continue.
- Write `market.json`: summary, buyer, user, geography, stage, 2-4 segments with a size hint. Mark size hints as estimates until the researcher sources them.

## 2. List the research questions

Cover at least: pain and its size, demand, competition, pricing / willingness to pay, regulation, trends, why now, white space, rising products, newcomer success. Add the playbook's space-specific questions. Phrase each as a question a source can answer ("Which tasks do RERA-registered developers file every quarter?"), not a topic.

## 3. Map questions → source types → named sources

1. For each question, list the source **types** that can answer it: government / regulatory, procurement and tenders, industry bodies, trade media, competitors (product, pricing, changelog), customer voice (reviews, forums, social, local-language video), demand signals (search trends, job posts), funding news and databases, academic, public data, public rails / platforms.
2. For each type, name **specific** sources with URLs. Start from the playbook list, then go beyond it: search for the state portal, the association, the subreddit, the app's review page, the exact job title on Naukri, the competitor's pricing page.
3. Check the registry: sources that yielded evidence in related runs (`productive_sources`) go first.

## 4. Vet every source

Score and record, per source:

| Field | Rule |
|---|---|
| `credibility` | 1-5. Primary/official = 5; reputable body or dataset = 4; trade media, competitor's own claims, review aggregates = 3; forums, social = 2; anonymous or SEO content = 1 |
| `recency` | Date range of the data. Flag anything older than 3 years for fast-moving questions |
| `bias` | Who benefits from the claim (vendor, association lobbying, investor PR) |
| `access` | free / freemium / paywalled / login / scrape. Prefer free; note when a paywalled source is replaceable |
| `india_relevance` | high / medium / low. Global sources are fine for benchmarks, not for Indian demand or pricing |

Open each URL (or search result) to confirm it exists and is about what you claim. Drop dead links.

## 5. Coverage rules

- Each question needs **≥3 independent source types** (three vendors' blogs count as one type).
- At least one local-language source when users or buyers work in Indian languages.
- At least one customer-voice and one demand-signal source per run.
- List anything you couldn't cover in `gaps`, with why.

Write `source_plan.json` (shape in the render-dashboard skill): `questions`, `sources` (`id`, `name`, `url`, `type`, `questions`, `why`, `credibility`, `recency`, `bias`, `access`, `india_relevance`), `gaps`.

## 6. Fixing checker gaps

When the orchestrator sends you the checker's numbered gap list, fix each item (add, replace or justify) and append a `changes` list to `source_plan.json` saying what you did per gap number. Don't remove good sources just to look different.

## 7. After research: yield and playbook proposals

Read `evidence.json`. Write `source_yield.json`: `{"productive": [{"name","url","type","evidence_count"}], "dry": [{"name","url","reason"}]}`. Write `playbook_proposals.md`: sources to add to the playbook (productive and not already listed), sources to demote (dry twice), new signals you noticed. Proposals only; the user decides.
