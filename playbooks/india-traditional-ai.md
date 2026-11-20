---
name: india-traditional-ai
space: AI products for traditional Indian industries - manufacturing, retail and kirana, construction, real estate, agriculture, logistics, MSME services and government
version: 1
---

# Playbook: Traditional industries in India adopting AI

Use this when the buyer is an Indian business or government body in a sector that still runs on paper, phone calls, WhatsApp and manual labour. The product sells AI that removes that work. It's a starting point for the source hunter. Every run should still find the specific state portal, association, trade forum and job title for its sector.

## Research questions (space-specific)

- Which tasks are still done by hand, on paper or on WhatsApp, and how many people-hours do they take?
- Which rule, filing or inspection forces this work, and what is the penalty for getting it wrong?
- Who signs the cheque: owner, CFO, site/plant head, a government department, or a lender? From which budget?
- How do they buy today: direct, via a dealer/channel partner, via GeM or a tender?
- Which public rails (UPI, ONDC, Account Aggregator, ULI, GSTN, e-invoicing, DigiLocker, Bhashini) could the product plug into?
- Which languages do the people doing the work use?

## Sources

| Type | Source | URL | Access | Notes |
|---|---|---|---|---|
| Government / regulatory | Government e-Marketplace (GeM) | https://gem.gov.in | free | What government buys, at what price, bid volumes |
| Government / regulatory | Central Public Procurement Portal | https://eprocure.gov.in | free | Central tenders; search by keyword and sector |
| Government / regulatory | State RERA portals (e.g. MahaRERA) | https://maharera.maharashtra.gov.in | free / scrape | Quarterly filings, registered projects, complaints |
| Government / regulatory | Ministry / regulator circulars (RBI, SEBI, BIS, CPCB, MoHUA, MoRTH) | https://www.rbi.org.in | free | Mandates that create compliance work |
| Government / regulatory | Udyam / MSME dashboards | https://msme.gov.in | free | MSME counts by state and sector |
| Government / data | data.gov.in, MOSPI (ASI, PLFS) | https://data.gov.in | free | Sizing: units, workers, output |
| Public rails | NPCI (UPI, ONDC stats), Sahamati (Account Aggregator), RBIH (ULI), Bhashini | https://www.npci.org.in | free | New rails to build on; adoption numbers |
| Industry bodies | CII, FICCI, NASSCOM, sector bodies (CREDAI, ACMA, SIAM, FISME, RAI, AIMO) | https://www.cii.in | free / members | Reports, pain surveys, member counts |
| Competitors & pricing | Indian vertical SaaS sites and pricing pages; Tracxn / Inc42 profiles | https://inc42.com | free / partly paywalled | Who is already selling, at what price |
| Customer voice | Trade forums, YouTube channels and WhatsApp/Telegram groups of the trade; IndiaMART reviews | https://www.indiamart.com | free | Workarounds, complaints, prices paid |
| Customer voice | Google Play reviews of Indian vertical apps | https://play.google.com | free / scrape | What existing tools fail at |
| Demand signals | Naukri / LinkedIn / Apna job posts for the manual role (e.g. "billing engineer", "QC inspector", "data entry") | https://www.naukri.com | free / scrape | Headcount spent on the task; salary = money at stake |
| Demand signals | Google Trends (India, Hindi and regional queries) | https://trends.google.com | free | Rising interest |
| Funding & newcomers | Entrackr, Inc42, YourStory funding news | https://entrackr.com | free | Recent raises, fast-growing newcomers |
| Academic | IIM / IIT working papers, ICRIER, NCAER | https://www.ncaer.org | free | Productivity and adoption studies |
| Local-language | Regional business press (Dainik Bhaskar, Lokmat, Eenadu business pages), vernacular YouTube | https://www.bhaskar.com | free | Voice of owners who don't write in English |

## Signals

- **Manual labour:** many job posts for a clerical or inspection role; teams of people doing the same lookup, entry or check.
- **Paperwork:** registers, measurement books, physical challans, stamped photos, scanned PDFs sent on WhatsApp.
- **Language friction:** workers speak Hindi or a regional language; the systems, forms or customers are in English.
- **Compliance pain:** a new or tightened rule, a deadline, penalties, or rejections (RERA, GST e-invoicing, BIS, EPR, labour codes).
- **Money at stake:** delayed payments, disputed bills, fines, working capital stuck, theft or wastage that someone can put a rupee number on.
- **New public rails:** a rail that makes a previously hard step cheap (UPI for payments, AA for financial data, ULI for lending data, ONDC for discovery, Bhashini for language). Build on new rails, like Razorpay on UPI.
- **Government pull:** GeM categories or tenders asking for this capability; scheme money (PLI, Smart Cities, PMAY).

## Scoring rubric

Score each criterion 1-5. Weights sum to 100. Total = sum(score x weight) / 5, out of 100. Every 4 or 5 must cite evidence ids.

| Criterion | Weight | 5 means | 1 means |
|---|---|---|---|
| Pain & money at stake | 20 | Rupee loss or cost is large, frequent and easy to point at | Annoyance, no number attached |
| Who buys & willingness to pay | 15 | Clear buyer with a budget line who already pays for something similar | Unclear who pays; users expect it free |
| Sales cycle | 10 | Owner-led or departmental purchase in weeks | Tender or board approval, 12+ months |
| Integration effort | 10 | Works from WhatsApp, photos, PDFs or a phone; no ERP integration | Needs deep integration with on-prem or custom systems |
| Competition & white space | 15 | No credible Indian or global product for this exact job | Funded incumbents already do this well |
| Why now (incl. public rails) | 15 | A new rule, rail or cost drop in the last 2 years makes it possible or necessary | Could have been built 10 years ago; nothing changed |
| Newcomer success | 5 | Recent startups in adjacent jobs are growing fast | No newcomer has gained traction in the sector |
| Need for change | 10 | Buyers say they want to change and are trying workarounds | Buyers are content with the status quo |

### As a secondary playbook

When another playbook is primary (e.g. B2B SaaS sold to Indian MSMEs), add and show separately:

- **Integration effort** (as above)
- **Language & literacy fit:** works for users who don't read English
- **Public rails leverage:** builds on UPI, ONDC, AA, ULI, GSTN or Bhashini

## Kill criteria

- Only buyer is government and the only route is a long tender with no pilot path.
- Value depends on data the buyer doesn't have digitally and won't capture.
- Price needed to make money is above what the segment pays for any software (check what they pay for Tally, Busy or similar).
- A large incumbent (Tata, Reliance Jio, Zoho, Tally, a big bank or a state agency) already bundles it for free or near-free.
- Needs a licence or approval the founder can't realistically get.
- The rail or rule the idea depends on is proposed but not live, with no date.

## Validation

- **Paid pilot:** 3-5 buyers pay for a 4-8 week pilot on their own data. Success: at least 2 convert or sign an LOI with a price.
- **Concierge test:** do the job by hand (with AI behind the scenes) for 5 customers via WhatsApp. Success: they send the next batch without being asked.
- **Channel test:** one dealer, CA firm or association agrees to introduce you to 10 members.
