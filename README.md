# Composio AI Product Ops: 100-App Toolkit Research & Buildability Audit

> **AI Product Ops Intern Take-Home Assignment**  
> **Author:** Adarsh Mishra (`Adarshhic`)  
> **Source Repository:** [https://github.com/Adarshhic/Product---Intern-Task](https://github.com/Adarshhic/Product---Intern-Task)  
> **Live Interactive Case Study:** [https://adarshhic.github.io/Product---Intern-Task/](https://adarshhic.github.io/Product---Intern-Task/)  
> **Primary Dataset:** `data/apps_research_dataset.json` (also exported as `data/apps_research_dataset.csv`)

---

## Executive Summary

Composio turns software applications into agent-callable tools. Before building a toolkit, we research auth protocols, developer gating, API surface breadth, and Model Context Protocol (MCP) status across target apps.

### Methodology & Honest Disclosure
* **Research Approach:** The research was **AI-assisted and curated**, combining initial extraction with **live Python network probes** (`requests`) against official documentation, active MCP registries, and developer portals.
* **Accuracy Measurement Disclosure:** *Pass 2 was checked against vendor docs by the candidate with AI assistance; accuracy is self-assessed against that ground truth, not independently audited.*
* **Strict Record Match Definition:** Strict record match requires all 5 core fields (primary auth method, self-serve status, API surface breadth, MCP status, and buildability verdict) to match verified ground truth simultaneously.
* **Runtime Verification:** `src/agent.py` and `src/verifier.py` execute real HTTP requests to verify URL reachability and detect bot-gated platforms (Cloudflare/Akamai WAF shields on Salesforce and PitchBook).
* **Where a Human Was Needed:** Human review resolved Cloudflare WAF bot blocks (403s), reconciled complex enterprise sales walls (DealCloud, Gladly, PitchBook), flagged non-SaaS CLI execution tools (Sherlock, Mermaid CLI), and caught fragile unofficial session cookie implementations (Otter AI).

---

## Recomputed Headline Metrics

All numbers below are mathematically recomputed directly from `data/apps_research_dataset.json`:

```
┌─────────────────────────────────┬──────────┬────────────────────────────────────────────────────────┐
│ Metric                          │ Count    │ Strategic Meaning for Composio                         │
├─────────────────────────────────┼──────────┼────────────────────────────────────────────────────────┤
│ 🚀 Ready for Agent Toolkits     │ 81% (81) │ 81 apps are Ready Today with documented public APIs    │
│ ⚠️ Feasible with Caveats         │ 10% (10) │ Require app review, high paywalls, or SigV4 signing    │
│ 🔒 Gated / Partner Required     │ 8% (8)   │ Require commercial contracts or manual sales clearance │
│ 🛑 Blocked (No Public API)      │ 1% (1)   │ Consumer-only platform with zero public API (Fanbasis) │
├─────────────────────────────────┼──────────┼────────────────────────────────────────────────────────┤
│ 🔓 Free Self-Serve / Trial      │ 74% (74) │ Instant developer keys without human gatekeepers       │
│ 💳 Paid Plan Only Self-Serve    │ 11% (11) │ Self-serve card checkout required for API keys        │
│ ⚡ Total Self-Serve Path        │ 85% (85) │ 85 apps have a self-serve path (74 free + 11 paid)     │
│ 🧱 Total Non-Self-Serve / Gated │ 15% (15) │ 9 Sales Walls + 5 Platform Review Gates + 1 No API     │
├─────────────────────────────────┼──────────┼────────────────────────────────────────────────────────┤
│ 🌐 Composio MCP Greenfield      │ 42% (42) │ Zero official or community MCP servers exist today     │
│ 📦 Existing MCP Ecosystem       │ 58% (58) │ 11 Official & Community + 47 Community MCP servers     │
└─────────────────────────────────┴──────────┴────────────────────────────────────────────────────────┘
```

> **Arithmetic Reconciliation:**  
> * **By Verdict:** 81 Ready Today + 10 Feasible with Caveats + 8 Gated / Partner Required + 1 Blocked (No API) = **100 apps**.  
> * **By Access:** 85 Self-Serve (74 Free Tier/Trial + 11 Paid Plan Only) + 15 Gated/Non-Self-Serve (9 Sales Walls + 5 Admin Approval Gates + 1 No API) = **100 apps**.  
> *(The 4-app difference between 81 Ready and 85 Self-Serve represents self-serve apps with integration caveats, such as local CLI requirements).*

---

## Macro Patterns: Insight Over Raw Table

### 1. The Dual-Track Auth Landscape
* **Primary Auth Distribution:** Recomputed strictly from `primary_auth` across all 100 apps (primary production protocol rule):
  * **API Key / Bearer Token:** 60% (60 apps)
  * **OAuth 2.0 / Managed OAuth:** 25% (25 apps)
  * **HTTP Basic Auth (Key/Secret):** 5% (5 apps)
  * **Local CLI / Process Execution:** 3% (3 apps: Sherlock, Mermaid CLI, Higgsfield CLI)
  * **Other Custom Auth (HMAC/SigV4/Hash/Session):** 6% (6 apps: Amazon SP-API, Paygent, Otter AI, etc.)
  * **None (No Public API):** 1% (1 app: Fanbasis)
  * **Total:** 60 + 25 + 5 + 3 + 6 + 1 = **100%**.
* *Composio Value:* Composio’s managed auth handles token refreshing, callback routing, and credential encryption, eliminating auth failures for autonomous agents.

### 2. The 15 Non-Self-Serve Apps Breakdown
The 15 apps that cannot be accessed via instant self-serve divide into:
1. **9 Institutional Sales Walls (9 apps):** DealCloud, Pylon, Gladly, Salesforce Commerce Cloud, Waterfall.io, Paygent Connect, iPayX, PitchBook, Otter AI.
2. **5 Platform App Review Moats (5 apps):** Google Ads, Meta Ads, LinkedIn Ads, Amazon SP-API, NotebookLM. Production access requires business verification and security policy audits.
3. **1 Closed Platform (1 app):** Fanbasis (consumer-only UI; zero documented developer API).

### 3. The 42% MCP Greenfield Opportunity
42% of target apps have **zero existing MCP server** in the ecosystem.
* **Top Greenfield Opportunities:** Front, Help Scout, Gorgias (Support), BigCommerce, Ecwid (Ecommerce), Smartsheet, Harvest (Productivity), Attio, Twenty (Modern CRMs).

### 4. Local CLI & Subprocess Frontier
Tools like **Sherlock** (OSINT username hunter) and **Mermaid CLI** (diagram generator) are open-source client-side CLI tools without hosted SaaS endpoints. Toolkits for these require sandboxed subprocess execution runners rather than standard HTTP requests.

---

## Accuracy Verification & Field-Level Progression

### 1. Full Dataset Progression (N=100)
Measured across each field dimension between initial naive extraction (Pass 1) and candidate-verified ground truth (Pass 2):
* **Buildability Verdict:** 78 / 100 (78.0%) &rarr; 98 / 100 (98.0%) [+20.0%]
* **Self-Serve Access Status:** 71 / 100 (71.0%) &rarr; 98 / 100 (98.0%) [+27.0%]
* **Primary Auth Method:** 67 / 100 (67.0%) &rarr; 98 / 100 (98.0%) [+31.0%]
* **Strict All-Field Match:** 51 / 100 (51.0%) &rarr; 98 / 100 (98.0%) [+47.0%]

### 2. Validation Samples (20 Apps Total)
We audit two distinct samples (10 reproducible random + 10 targeted edge cases):
* **Random Representative Sample (N=10, Seed=42 via `random.Random(42)`):**
  - Pass 1 Strict Accuracy: 7 / 10 (70.0%)
  - Pass 2 Verified Accuracy: 10 / 10 (100.0%)
  - *Sampled Apps:* Attio, Front, Pylon, Help Scout, Aircall, Meta Ads, Klaviyo, Plaid, Xero, Reducto.
* **Edge-Case & Gated Sample (N=10, Purposefully Selected &mdash; Not Representative):**
  - Pass 1 Strict Accuracy: 0 / 10 (0.0%)
  - Pass 2 Verified Accuracy: 8 / 10 (80.0%, 2 residual caveats)
  - *Sampled Apps:* DealCloud, Gladly, Google Ads, Amazon SP-API, Fanbasis, Sherlock, Otter AI, NotebookLM, PitchBook, Paygent Connect.
* **Combined 20-App Audit Sample:**
  - Pass 1: 7 / 20 (35.0%) &rarr; Pass 2: 18 / 20 (90.0%, 2 residual caveats).

### 3. Hard Cases & Residual Uncertainty (2 Apps / 2.0%)
The 98.0% verified strict accuracy represents 98 out of 100 records confirmed against vendor docs (100 minus Otter AI and NotebookLM = 98):
1. **#92 Otter AI (`wrong` in Pass 1):** Agent hallucinated an official public REST API; human inspection revealed community integrations rely on reverse-engineered user session cookies (`auth_token`) that break upon logout.
2. **#91 NotebookLM (`uncertain`):** Sharp separation between the consumer app (zero public API) and Google Cloud Discovery Engine APIs; agent claimed standard API key access, missing the enterprise GCP requirement.
3. **#50 Fanbasis (`right-but-hard`):** Agent correctly flagged this platform as Blocked (No API); toolkit integration strictly requires browser-use automation. Confirmed accurate.
4. **#90 PitchBook (`right-but-hard`):** Agent correctly identified Gated / Partner Required; verification was hard because the portal is shielded by Cloudflare Enterprise WAF (HTTP 403 on CLI) and pricing is undisclosed institutional sales. Confirmed accurate.

---

## How to Run Locally

### 1. Setup Environment
```bash
git clone https://github.com/Adarshhic/Product---Intern-Task.git
cd Product---Intern-Task
pip install -r requirements.txt
```

### 2. Run Test Suite
```bash
python -m unittest discover tests
```

### 3. Run Live Tool Probes & Pipeline
```bash
# Run real HTTP evidence probes on sample of 10 apps
python run.py --sample 10

# Run full automated verification, error taxonomy, and pattern clustering
python run.py --all

# Regenerate HTML case study
python src/build_html.py
```
