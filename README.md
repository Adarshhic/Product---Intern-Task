# Composio AI Product Ops: 100-App Toolkit Research & Buildability Audit

> **AI Product Ops Intern Take-Home Assignment**  
> **Author:** Adarsh Mishra (`Adarshhic`)  
> **Source Repository:** [https://github.com/Adarshhic/Product---Intern-Task](https://github.com/Adarshhic/Product---Intern-Task)  
> **Live Interactive Case Study:** [https://adarshhic.github.io/Product---Intern-Task/](https://adarshhic.github.io/Product---Intern-Task/)  
> **Primary Dataset:** `data/apps_research_dataset.json` (also exported as `data/apps_research_dataset.csv`)

---

## Executive Summary

Composio turns software applications into agent-callable tools. Before building a toolkit, we research auth protocols, developer gating, API surface breadth, and Model Context Protocol (MCP) status across target apps.

### Methodology & System Architecture
* **Research Approach:** The research was **AI-assisted and curated**, combining initial extraction with **live Python network probes** (`requests`) against official documentation, active MCP registries, and developer portals.
* **Runtime Verification:** `src/agent.py` and `src/verifier.py` execute real HTTP requests to verify URL reachability and detect bot-gated platforms (WAF shields on Salesforce and PitchBook).
* **Single Defensible Accuracy Story:** Rather than claiming 100% automated accuracy, we measured field-level accuracy across all 100 apps and audited two distinct samples (a seeded random sample of 20 and a targeted edge-case sample of 13), documenting how verification loops improved strict record accuracy from **23.0% (Pass 1)** to **96.0% (Pass 2)**, with 4 honest residual edge cases.

---

## Recomputed Headline Metrics

All numbers below are computed directly from `data/apps_research_dataset.json`:

```
┌─────────────────────────────────┬──────────┬────────────────────────────────────────────────────────┐
│ Metric                          │ Count    │ Strategic Meaning for Composio                         │
├─────────────────────────────────┼──────────┼────────────────────────────────────────────────────────┤
│ 🚀 Ready for Agent Toolkits     │ 81% (81) │ Direct, unblocked public APIs ready for toolkits today │
│ ⚠️ Feasible with Caveats         │ 10% (10) │ Require app review, high paywalls, or SigV4 signing    │
│ 🔒 Gated / Partner Required     │ 8% (8)   │ Require commercial contracts or manual sales clearance │
│ 🛑 Blocked (No Public API)      │ 1% (1)   │ Consumer-only platform with zero public API (Fanbasis) │
├─────────────────────────────────┼──────────┼────────────────────────────────────────────────────────┤
│ 🔓 Free Self-Serve / Trial      │ 74% (74) │ Instant developer keys without human gatekeepers       │
│ 💳 Paid Plan Only Self-Serve    │ 11% (11) │ Self-serve card checkout required for API keys        │
│ 🧱 Total Non-Self-Serve / Gated │ 15% (15) │ 9 Sales Walls + 5 Platform Review Gates + 1 No API     │
├─────────────────────────────────┼──────────┼────────────────────────────────────────────────────────┤
│ 🌐 Composio MCP Greenfield      │ 42% (42) │ Zero official or community MCP servers exist today     │
│ 📦 Existing MCP Ecosystem       │ 58% (58) │ 11 Official & Community + 47 Community MCP servers     │
└─────────────────────────────────┴──────────┴────────────────────────────────────────────────────────┘
```

---

## Macro Patterns: Insight Over Raw Table

### 1. The Dual-Track Auth Landscape
- **Developer Infra, Scraping & AI (53%)** standardizes heavily on **Bearer API Keys** with rapid developer onboarding (e.g. Supabase, Firecrawl, SendGrid, Reducto).
- **Enterprise CRM, Support & Messaging (31%)** enforces **OAuth 2.0 with PKCE and token rotation** (Salesforce, HubSpot, Slack, Intercom).
- *Composio Value:* Composio’s managed auth handles token refreshing, callback routing, and credential encryption, reducing failure rates for autonomous agents.

### 2. The 15 Non-Self-Serve Apps Breakdown
The 15 apps that cannot be accessed via instant self-serve divide into:
1. **9 Institutional Sales Walls (9 apps):** DealCloud, Pylon, Gladly, Salesforce Commerce Cloud, Waterfall.io, Paygent Connect, iPayX, PitchBook, Otter AI. No public self-serve signup exists.
2. **5 Platform App Review Moats (5 apps):** Google Ads, Meta Ads, LinkedIn Ads, Amazon SP-API, NotebookLM. Developer accounts are self-serve, but production traffic requires business verification and policy audits.
3. **1 Closed Platform (1 app):** Fanbasis (consumer-only UI; no documented developer API).

### 3. The 42% MCP Greenfield Opportunity
42% of target apps have **zero existing MCP server** in the ecosystem.
- **Top Greenfield Opportunities:** Front, Help Scout, Gorgias (Support), BigCommerce, Ecwid, Gumroad (Ecommerce), Smartsheet, Harvest (Productivity), Attio, Copper (Modern CRMs).

### 4. The AI App Paradox
Consumer AI applications (NotebookLM, Otter AI) have viral demand for toolkits, but possess **immature public API surfaces**.
- Otter AI community MCPs rely on reverse-engineered user session cookies.
- NotebookLM enterprise access is routed via Google Cloud Vertex AI extensions.
- *Solution:* Composio can provide hybrid toolkits combining browser automation and session runners until official developer APIs launch.

### 5. The Native CLI & Local Subprocess Frontier
Apps like **Sherlock** (OSINT username hunter) and **Mermaid CLI** (diagram generator) are open-source client-side CLI tools without hosted SaaS endpoints. Toolkits for these require subprocess / container execution wrappers rather than standard HTTP requests.

---

## Accuracy Verification & Field-Level Progression

### 1. Full Dataset Progression (N=100)
Measured across each field dimension between initial naive extraction (Pass 1) and verified ground truth (Pass 2):
* **Buildability Verdict:** 78 / 100 (78.0%) &rarr; 98 / 100 (98.0%)
* **Self-Serve Access Status:** 71 / 100 (71.0%) &rarr; 98 / 100 (98.0%)
* **Primary Auth Method:** 31 / 100 (31.0%) &rarr; 98 / 100 (98.0%)
* **Strict All-Field Match:** 23 / 100 (23.0%) &rarr; 96 / 100 (96.0%)

### 2. Two Distinct Validation Samples
* **Random Representative Sample (N=20, Seed=42):**
  - Pass 1 Strict Accuracy: 5 / 20 (25.0%)
  - Pass 1 Verdict Accuracy: 17 / 20 (85.0%)
  - Pass 2 Verified Accuracy: 20 / 20 (100.0%)
  - *Sampled Apps:* Attio, Twenty, Intercom, Front, Pylon, Help Scout, WhatsApp, Aircall, Vonage, Meta Ads, Klaviyo, Apify, Supabase, Sentry, Airtable, Linear, Asana, Plaid, Brex, Reducto.
* **Edge-Case & Gated Sample (N=13, Purposefully Selected &mdash; Not Representative):**
  - Pass 1 Strict Accuracy: 0 / 13 (0.0%)
  - Pass 1 Verdict Accuracy: 1 / 13 (7.7%)
  - Pass 2 Verified Accuracy: 11 / 13 (84.6%)
  - *Sampled Apps:* DealCloud, Gladly, WhatsApp, Google Ads, Meta Ads, Amazon SP-API, Fanbasis, Ahrefs, Sherlock, Paygent, PitchBook, NotebookLM, Otter AI.

### 3. Where the Pipeline Was Defeated / Residual Caveats (4 Apps / 4%)
1. **#92 Otter AI:** No official public developer REST API; existing community MCP servers rely on reverse-engineered user session cookies (`auth_token`).
2. **#91 NotebookLM:** Consumer web app lacks public APIs; programmatic automation requires Google Cloud Gemini Notebook Enterprise and Vertex AI Discovery Engine permissions.
3. **#50 Fanbasis:** Only platform in the 100 with zero developer endpoints; requires browser-use web automation.
4. **#90 PitchBook:** Shields developer portal behind Cloudflare Enterprise WAF (HTTP 403 on automated requests); pricing requires annual institutional sales contracts.

---

## How to Run Locally

### 1. Setup Environment
```bash
git clone https://github.com/Adarshhic/Product---Intern-Task.git
cd Product---Intern-Task
python -m venv venv
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/macOS:
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Test Suite
```bash
python -m unittest discover tests
```

### 3. Run Live Tool Probes & Pipeline
```bash
# Run real HTTP evidence probes on 10 apps
python run.py --sample 10

# Run full automated verification, error taxonomy, and pattern clustering
python run.py --all

# Regenerate HTML case study
python src/build_html.py
```

---

## Limitations & Honest Disclosure

1. **Agent Runtime Scope:** `src/agent.py` executes live network requests, status verification, and schema validation over a curated research dataset. It does not invoke an LLM from scratch at runtime.
2. **Bot-Shielded Portals:** Salesforce and PitchBook return HTTP 403 to automated command-line scripts due to WAF protection (Akamai/Cloudflare); both were confirmed 200 in real browser sessions.
3. **Residual Uncertainty:** 4 platforms (Otter AI, NotebookLM, Fanbasis, PitchBook) remain nuanced edge cases requiring either enterprise sales agreements or browser automation.
