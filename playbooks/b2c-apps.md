---
name: b2c-apps
space: Consumer apps and digital products - mobile, web, creator tools, subscriptions, consumer AI
version: 1
---

# Playbook: B2C apps

Use this when the user and the payer are individual consumers. Revenue comes from subscriptions, in-app purchases, ads or commissions. It's a starting point for the source hunter. Every run should still find the specific chart category, subreddit and competitor review pages for its brief.

## Research questions (space-specific)

- Which apps in this category are rising in the charts, and which are new (launched in the last 2 years)?
- What do users complain about in 1-3 star reviews of the leaders?
- How do people find these apps: search, social, word of mouth, app store browse?
- What do comparable apps charge, and what is their estimated revenue?
- How long do users stay (retention signals: reviews mentioning daily use, streaks, cancellations)?
- In the target geography, what price points and payment methods work (e.g. UPI autopay, ₹ pricing tiers in India)?

## Sources

| Type | Source | URL | Access | Notes |
|---|---|---|---|---|
| App store charts | Apple App Store top charts by country and category | https://apps.apple.com/in/charts/iphone | free | Rank, new entrants |
| App store charts | Google Play top charts | https://play.google.com/store/apps/top | free | Rank, installs ranges |
| Revenue estimates | Appfigures public top-grossing lists and blog | https://appfigures.com/top-apps | free / paywalled | Revenue and download estimates |
| Revenue estimates | Sensor Tower public reports and blog | https://sensortower.com/blog | free | Category trends, top earners |
| Revenue estimates | data.ai (Sensor Tower) State of Mobile report | https://www.data.ai/en/go/state-of-mobile-2024 | free with form | Market-level spend by country |
| Customer voice | App Store and Play Store reviews of competitors | https://play.google.com | free / scrape | Complaints, missing features |
| Customer voice | Reddit (category subreddits, r/india, r/IndianTeenagers etc.) | https://www.reddit.com | free | Unfiltered pain, workarounds |
| Customer voice | YouTube and Instagram comments on category creators | https://www.youtube.com | free | What people ask for |
| Demand signals | Google Trends | https://trends.google.com | free | Rising search interest |
| Demand signals | Keyword tools (Google Keyword Planner, AppTweak / ASO free tools) | https://ads.google.com/home/tools/keyword-planner | free with login | Search volume = discoverability |
| Competitors & pricing | Competitor websites, paywall screenshots, pricing pages | | free | Price points and plan design |
| Funding & newcomers | Product Hunt, Crunchbase news, Entrackr / Inc42 (India) | https://www.producthunt.com | free | New launches and raises |
| Industry reports | RedSeer, KPMG India media and entertainment report, Bain India consumer reports | https://redseer.com | free / partly paywalled | Market size, user counts |
| Local-language | Regional-language app reviews, vernacular creator channels | | free | Bharat users' needs |

## Signals

- **Rising apps:** an app climbing the category chart over 3-6 months, especially a small team.
- **Newcomer success:** an app under 2 years old in the top 50 grossing, or a solo/indie app with public revenue numbers.
- **Complaints:** repeated 1-3 star reviews on the same problem (price hike, ads, missing language, bugs after update).
- **Workarounds:** people using spreadsheets, Notes, WhatsApp groups or ChatGPT prompts to do the job.
- **Platform shifts:** new OS features, on-device AI, new payment rails (UPI autopay) that open a gap.
- **Search without a good answer:** high search volume with weak or old apps in the results.

## Industry screen

Used by the industry scout before any deep research. Score each candidate 1-5; weights sum to 100; total = sum(score x weight) / 5. Every 4 or 5 needs a signal with a URL. Shortlist about 3.

Candidates are **consumer segments** (who, with which need), e.g. "Indian Gen-Z exam aspirants", "new parents in metro India", "US freelancers managing taxes".

| Criterion | Weight | 5 means | 1 means |
|---|---|---|---|
| Spending power & willingness to pay | 20 | Segment already pays for apps or subscriptions for this need | Expects everything free; ad-supported only |
| Size & growth | 15 | Large segment that is visibly growing | Small or shrinking |
| Reachability (organic channels) | 20 | Clear organic channels: search terms, communities, creators, app-store keywords | Only reachable through paid ads |
| Competition density (low is good) | 15 | Top charts for the need are thin or dated | Dominated by well-funded, well-reviewed apps |
| Unmet complaints | 15 | Many recent 1-3 star reviews and forum threads about the same gap | Users seem satisfied |
| Newcomer success | 15 | Apps launched in the last 2 years are climbing charts or revenue estimates | No newcomer has broken in |

Example longlist: students and exam prep, fitness and health tracking, parenting, personal finance, language learning, dating and social, travel planning, small creators, pet owners, older adults and caregivers, hobby learners, home and cooking.

## Scoring rubric

Score each criterion 1-5. Weights sum to 100. Total = sum(score x weight) / 5, out of 100. Every 4 or 5 must cite evidence ids.

| Criterion | Weight | 5 means | 1 means |
|---|---|---|---|
| Trends & demand | 15 | Search and chart interest rising for 6+ months | Flat or falling interest |
| Revenue opportunity | 15 | Comparable apps earn meaningful revenue in the target market | Category barely monetises |
| Willingness to pay | 15 | Users already pay for similar apps at the target price | Users expect it free; ads-only |
| Discoverability (ASO / SEO / social) | 15 | Clear search terms with weak results, or a natural social loop | Only reachable via paid ads |
| Retention | 15 | Daily or weekly habit; value grows with use | One-time use, then uninstall |
| Competition & white space | 10 | Leaders have clear, repeated complaints; no app fixes them | Strong, loved leaders cover the job |
| Rising apps & newcomer success | 10 | New or small apps are climbing fast in this category | Charts locked by incumbents for years |
| Need for change | 5 | Users actively look for alternatives | Users are content |

### As a secondary playbook

When another playbook is primary, add and show separately:

- **Discoverability (ASO / SEO / social)**
- **Retention**

## Kill criteria

- The job is a feature the platform owner (Apple, Google, WhatsApp, Instagram) or the market leader can ship in one release, and is likely to.
- No organic channel: the only way to get users is paid ads, and target-market price can't cover the cost per install.
- Users don't pay for anything in the category in the target geography.
- Value needs a large network before the first user gets any benefit.
- Health, finance or kids' data without a credible path through the rules (DPDP Act, RBI, app store policies).

## Validation

- **Landing page with paid sign-ups:** a page with the promise and price, driven by a small ad spend or community posts. Success: 3%+ of visitors pre-pay or put down a deposit (or 10%+ join a waitlist with a price shown).
- **Fake-door test in a community:** post the idea where the users are; count DMs and sign-ups.
- **Concierge MVP:** deliver the result by hand for 20 users for 2 weeks. Success: 40%+ still active in week 2.
