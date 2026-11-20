---
name: b2b-saas
space: Software sold to businesses - horizontal and vertical SaaS, developer tools, AI agents for business workflows, marketplace apps
version: 1
---

# Playbook: B2B SaaS

Use this when a business pays a recurring fee for software. It's a starting point for the source hunter. Every run should still find the specific review categories, marketplaces and job titles for its brief.

## Research questions (space-specific)

- What do customers of the incumbents complain about (price, complexity, support, missing features)?
- What does the job cost today: tool spend plus the people doing it by hand?
- Who buys and who uses? Are they the same person?
- How long is the sales cycle, and who has to approve?
- What would a customer lose by switching (data, integrations, retraining)?
- Which platforms or APIs launched or changed recently (new APIs, AI models, marketplace openings, price hikes)?

## Sources

| Type | Source | URL | Access | Notes |
|---|---|---|---|---|
| Customer voice | G2 category pages and 1-3 star reviews | https://www.g2.com | free / scrape | Complaints, switching reasons |
| Customer voice | Capterra / GetApp reviews | https://www.capterra.com | free | SMB voice |
| Customer voice | Reddit (r/SaaS, r/sysadmin, role subreddits like r/accounting, r/sales) | https://www.reddit.com | free | Workarounds, tool rants |
| Competitors & pricing | Incumbent pricing pages (and Wayback Machine for price history) | https://web.archive.org | free | Price hikes, plan changes |
| Integration marketplaces | Salesforce AppExchange | https://appexchange.salesforce.com | free | Gaps, install counts, reviews |
| Integration marketplaces | Shopify App Store | https://apps.shopify.com | free | Merchant pain, reviews, pricing |
| Integration marketplaces | Slack Marketplace, Atlassian Marketplace, HubSpot, Zoho Marketplace | https://slack.com/marketplace | free | Platform gaps |
| Demand signals | Job posts (LinkedIn, Naukri, Indeed) for the manual role or tool skill | https://www.linkedin.com/jobs | free / scrape | Headcount spent on the job |
| Demand signals | Google Trends, keyword tools | https://trends.google.com | free | Search for "<tool> alternative" |
| Newcomers | Indie Hackers (products with public revenue) | https://www.indiehackers.com/products | free | Small teams making money |
| Newcomers | Product Hunt launches | https://www.producthunt.com | free | New entrants and reception |
| Funding & newcomers | Crunchbase news, TechCrunch, Entrackr / Inc42 (India) | https://news.crunchbase.com | free | Raises in the category |
| Platform shifts | Developer changelogs and API docs of platforms in the workflow | | free | New APIs that open a wedge |
| Industry reports | SaaS benchmarks (KeyBanc, OpenView archives, SaaS Capital), Bessemer State of the Cloud | https://www.saas-capital.com/research | free | ACV, churn, CAC norms |

## Signals

- **Incumbent bad reviews:** repeated complaints on G2/Capterra about the same thing, especially recent ones.
- **Spreadsheet workarounds:** people describing Excel, Google Sheets, Airtable or email doing the job.
- **Price hikes:** an incumbent raised prices or removed a cheaper plan; "<tool> alternative" searches rising.
- **New APIs / platform shifts:** a new API, AI model, marketplace or regulation that makes a narrow tool possible.
- **Job posts for the manual role:** companies hiring people to do what software could do.
- **Unbundling:** one module of a big suite used heavily and disliked; a focused tool can win.

## Industry screen

Used by the industry scout before any deep research. Score each candidate 1-5; weights sum to 100; total = sum(score x weight) / 5. Every 4 or 5 needs a signal with a URL. Shortlist about 3.

Candidates are **verticals or job functions** (e.g. "independent dental clinics", "finance teams at 50-500 person companies", "Shopify merchants doing 1-10 crore").

| Criterion | Weight | 5 means | 1 means |
|---|---|---|---|
| Number of businesses & budget | 20 | Many businesses with a budget line for software | Few buyers or no software budget |
| Spreadsheet / manual workarounds | 15 | Core work still runs on Excel, email or WhatsApp | Already well served by software |
| Incumbent dissatisfaction | 15 | Bad G2/Capterra reviews, price-hike complaints, ignored segment | Users happy with incumbents |
| Reachability | 15 | Reachable through marketplaces, communities, associations or search | Only via enterprise field sales |
| Sales cycle | 15 | Buyer is the user or the owner; buys in weeks | Committee purchase, 6+ months |
| Platform shift / why now | 10 | A new API, rule or platform change in the last 2 years | Nothing has changed |
| Newcomer success | 10 | Startups launched in the last 3 years are growing in this vertical | No newcomer traction |

Example longlist: clinics, law firms, accounting practices, agencies, e-commerce merchants, logistics operators, schools, property managers, recruiters, field-service businesses, finance teams, HR teams, sales teams.

## Scoring rubric

Score each criterion 1-5. Weights sum to 100. Total = sum(score x weight) / 5, out of 100. Every 4 or 5 must cite evidence ids.

| Criterion | Weight | 5 means | 1 means |
|---|---|---|---|
| Pain & revenue opportunity | 15 | Costly, frequent job with a large number of businesses doing it | Rare job or tiny market |
| ACV (annual contract value) | 15 | ACV fits the sales motion (high ACV with sales, or low ACV with self-serve) | ACV too low for sales, too complex for self-serve |
| Buyer = user | 10 | The person who feels the pain can buy with a card | Separate buyer who doesn't feel the pain |
| Sales cycle | 10 | Days to weeks, no procurement | 6+ months, security reviews, committees |
| Switching cost (in our favour) | 10 | Easy to switch in; hard to switch away once in use | Customers locked into the incumbent |
| Churn risk (low is good) | 10 | Embedded in a recurring workflow; system of record | Project-based use; cancelled after the job is done |
| Competition & white space | 15 | Incumbents disliked or absent for this segment | Well-loved incumbents serve this segment |
| Trends & why now | 10 | A recent platform, API, price or rule change opens the gap | Nothing changed recently |
| Newcomer success | 5 | Small teams in the category have public revenue or fast growth | No newcomer traction |

### As a secondary playbook

When another playbook is primary (e.g. AI for Indian manufacturers sold as SaaS), add and show separately:

- **ACV**
- **Switching cost (in our favour)**
- **Churn risk (low is good)**

## Kill criteria

- The job is a checkbox feature the incumbent platform will add (or just added) for free.
- ACV and sales motion don't fit: needs enterprise sales but ACV is SMB-sized.
- Buyers churn when the project ends; no recurring workflow.
- Depends on one platform's API that the platform restricts or competes with.
- Category has 10+ funded competitors with no clear underserved segment.

## Validation

- **Paid pilots or LOIs:** 5 target companies agree to pay (or sign an LOI with a price) for a pilot. Success: at least 3.
- **Problem interviews with a price:** 15 interviews with buyers; ask for the current spend and show a price. Success: 5+ ask for access.
- **Marketplace listing or landing page:** list a minimal app or a "request access" page in the relevant marketplace. Success: set a sign-up count and timeframe in advance.
