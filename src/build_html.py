"""
HTML Case Study Generator: Composio AI Product Ops Take-Home.
Completely offline-first: Zero external CDN dependencies (no Tailwind CDN, no Chart.js CDN, no Google Fonts CDN).
Standard system fonts, pure inline CSS with custom theme toggle, SVG/CSS charts, responsive table.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

def generate_html():
    with open(DATA_DIR / "apps_research_dataset.json", "r", encoding="utf-8") as f:
        dataset = json.load(f)
    with open(DATA_DIR / "verification_report.json", "r", encoding="utf-8") as f:
        verification = json.load(f)
    with open(DATA_DIR / "pattern_analysis.json", "r", encoding="utf-8") as f:
        patterns = json.load(f)

    dataset_json_str = json.dumps(dataset)

    # Derived headline numbers
    total = patterns["metadata"]["total_apps"]
    ready_count = patterns["headline_metrics"]["ready_for_agent_today_count"]
    ready_pct = int(patterns["headline_metrics"]["ready_for_agent_today_pct"])
    feasible_count = patterns["headline_metrics"]["feasible_with_caveats_count"]
    feasible_pct = int(patterns["headline_metrics"]["feasible_with_caveats_pct"])
    gated_count = patterns["headline_metrics"]["gated_partner_required_count"]
    gated_pct = int(patterns["headline_metrics"]["gated_partner_required_pct"])
    blocked_count = patterns["headline_metrics"]["blocked_no_api_count"]
    blocked_pct = int(patterns["headline_metrics"]["blocked_no_api_pct"])
    free_ss_count = patterns["headline_metrics"]["free_self_serve_count"]
    free_ss_pct = int(patterns["headline_metrics"]["free_self_serve_pct"])
    paid_ss_count = patterns["headline_metrics"]["paid_self_serve_count"]
    paid_ss_pct = int(patterns["headline_metrics"]["paid_self_serve_pct"])
    total_gated_count = patterns["headline_metrics"]["total_gated_non_self_serve_count"]
    total_gated_pct = int(patterns["headline_metrics"]["total_gated_non_self_serve_pct"])
    greenfield_count = patterns["headline_metrics"]["composio_greenfield_count"]
    greenfield_pct = int(patterns["headline_metrics"]["composio_greenfield_pct"])

    p1_strict = verification["full_dataset_pass1_strict_pct"]
    p2_strict = verification["full_dataset_pass2_strict_pct"]
    residual_count = verification["residual_unresolved_count"]
    residual_pct = verification["residual_unresolved_pct"]

    # Hits and misses samples for the verification section
    sample_hits_misses = [
        {
            "app": "Stripe",
            "cat": "Finance and Fintech",
            "p1": "API Key | Self-Serve | Ready Today",
            "p2": "API Key (Bearer) | Self-Serve | Ready Today",
            "status": "Hit",
            "why": "Standard developer platform correctly identified in Pass 1 and verified in Pass 2."
        },
        {
            "app": "Slack",
            "cat": "Communication",
            "p1": "OAuth2 | Self-Serve | Ready Today",
            "p2": "OAuth2 / Bot Token | Self-Serve | Ready Today",
            "status": "Hit",
            "why": "Well-documented Bot Token and OAuth 2.0 flow verified against official docs."
        },
        {
            "app": "DealCloud",
            "cat": "CRM and Sales",
            "p1": "API Key | Self-Serve | Ready Today",
            "p2": "API Key / OAuth2 | Gated (Sales Wall) | Gated / Partner Required",
            "status": "Corrected Miss",
            "why": "Pass 1 hallucinated self-serve access; human review caught mandatory enterprise sales contract."
        },
        {
            "app": "Gladly",
            "cat": "Customer Support",
            "p1": "API Key | Self-Serve | Ready Today",
            "p2": "API Token | Gated (Sales Wall) | Gated / Partner Required",
            "status": "Corrected Miss",
            "why": "Pass 1 missed enterprise customer onboarding requirement; corrected in Pass 2."
        },
        {
            "app": "Sherlock",
            "cat": "Developer Tools",
            "p1": "REST API | Self-Serve | Ready Today",
            "p2": "Local CLI / Python Script | Self-Serve | Feasible with Caveats",
            "status": "Corrected Miss",
            "why": "Pass 1 assumed remote SaaS cloud endpoints; Pass 2 verified it runs as a local CLI subprocess."
        },
        {
            "app": "Attio",
            "cat": "CRM and Sales",
            "p1": "Generic API Key | Self-Serve | Ready Today",
            "p2": "API Key (Bearer) + OpenAPI | Self-Serve | Ready Today",
            "status": "Hit",
            "why": "Bearer token specification and OpenAPI v3 definition verified on live docs."
        }
    ]

    sample_rows_html = ""
    for s in sample_hits_misses:
        badge = '<span class="status-badge hit">Hit</span>' if s['status'] == 'Hit' else '<span class="status-badge corrected">Corrected Miss</span>'
        sample_rows_html += f"""<tr>
          <td><strong>{s['app']}</strong><br><span class="muted text-xs">{s['cat']}</span></td>
          <td class="font-mono text-xs">{s['p1']}</td>
          <td class="font-mono text-xs">{s['p2']}</td>
          <td>{badge}</td>
          <td class="text-xs">{s['why']}</td>
        </tr>"""

    html_content = f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Composio AI Product Ops: 100-App Agent Toolkit Research & Macro Patterns</title>
  <meta name="description" content="AI Product Ops Take-Home: 100-app toolkit research, buildability audit, macro patterns, and verification pipeline for Composio.">
  
  <!-- JSON-LD for Agent & Search Engine Discoverability -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Dataset",
    "name": "Composio 100-App Agent Toolkit Research Dataset",
    "description": "Comprehensive audit of 100 SaaS applications evaluating authentication protocols, self-serve access, API surface, MCP availability, and toolkit buildability.",
    "creator": {{
      "@type": "Person",
      "name": "Adarsh Mishra"
    }},
    "license": "https://creativecommons.org/licenses/by/4.0/",
    "isAccessibleForFree": true,
    "variableMeasured": ["auth_methods", "self_serve_status", "api_surface", "mcp_status", "buildability_verdict", "main_blocker"]
  }}
  </script>

  <style>
    /* ==========================================================================
       OFFLINE SYSTEM DESIGN SYSTEM: PALETTE & BASE VARIABLES
       Terracotta: #CC8161 | Obsidian: #040507 | Stone: #DFDAD4 | Light: #EFEFEF
       ========================================================================== */
    :root {{
      --bg: #040507;
      --bg-card: #0b0e14;
      --bg-card-hover: #121620;
      --bg-surface: #10141e;
      --bg-nav: rgba(4, 5, 7, 0.92);
      --text: #EFEFEF;
      --text-muted: #DFDAD4;
      --text-dim: #9ba1ad;
      --border: rgba(223, 218, 212, 0.16);
      --border-focus: #CC8161;
      --accent: #CC8161;
      --accent-dim: rgba(204, 129, 97, 0.15);
      --accent-hover: #b86d4e;
      --stone: #DFDAD4;
      --stone-dim: rgba(223, 218, 212, 0.12);
      
      --ready-color: #22c55e;
      --ready-bg: rgba(34, 197, 94, 0.12);
      --caveat-color: #f59e0b;
      --caveat-bg: rgba(245, 158, 11, 0.12);
      --gated-color: #f43f5e;
      --gated-bg: rgba(244, 63, 94, 0.12);
      --blocked-color: #94a3b8;
      --blocked-bg: rgba(148, 163, 184, 0.12);

      --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      --font-mono: ui-monospace, "Cascadia Code", "Source Code Pro", Menlo, Consolas, monospace;
      --space-1: 4px;
      --space-2: 8px;
      --space-3: 12px;
      --space-4: 16px;
      --space-5: 24px;
      --space-6: 32px;
      --space-8: 48px;
      --space-10: 64px;
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 14px;
      --radius-full: 9999px;
      --max-width: 1280px;
    }}

    [data-theme="light"] {{
      --bg: #F7F7F6;
      --bg-card: #FFFFFF;
      --bg-card-hover: #F2EFEB;
      --bg-surface: #EBE7E2;
      --bg-nav: rgba(247, 247, 246, 0.94);
      --text: #17181c;
      --text-muted: #3d424b;
      --text-dim: #606674;
      --border: rgba(4, 5, 7, 0.14);
      --border-focus: #B85D3B;
      --accent: #B85D3B;
      --accent-dim: rgba(184, 93, 59, 0.12);
      --accent-hover: #9e4c2d;
      --stone: #625c56;
      --stone-dim: rgba(98, 92, 86, 0.1);
      
      --ready-color: #16a34a;
      --ready-bg: rgba(22, 163, 74, 0.12);
      --caveat-color: #d97706;
      --caveat-bg: rgba(217, 119, 6, 0.12);
      --gated-color: #e11d48;
      --gated-bg: rgba(225, 29, 72, 0.12);
      --blocked-color: #64748b;
      --blocked-bg: rgba(100, 116, 139, 0.12);
    }}

    /* Global Reset & Typography */
    *, *::before, *::after {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    html {{
      font-size: 16px;
      scroll-behavior: smooth;
      background-color: var(--bg);
      color: var(--text);
      font-family: var(--font-sans);
      line-height: 1.5;
      text-rendering: optimizeLegibility;
      -webkit-font-smoothing: antialiased;
    }}

    body {{
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
      width: 100%;
    }}

    /* Skip Link for Accessibility & Speed */
    .skip-link {{
      position: absolute;
      top: -100px;
      left: 16px;
      background: var(--accent);
      color: #040507;
      padding: 8px 16px;
      font-weight: 700;
      border-radius: var(--radius-sm);
      z-index: 1000;
      text-decoration: none;
      transition: top 0.2s ease;
    }}
    .skip-link:focus {{
      top: 16px;
    }}

    /* Navigation */
    header.sticky-nav {{
      position: sticky;
      top: 0;
      z-index: 100;
      background: var(--bg-nav);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border);
    }}
    .nav-container {{
      max-width: var(--max-width);
      margin: 0 auto;
      padding: 0 var(--space-4);
      height: 60px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: var(--space-4);
    }}
    .nav-brand {{
      display: flex;
      align-items: center;
      gap: var(--space-3);
      text-decoration: none;
      color: var(--text);
      font-weight: 800;
      font-size: 1.125rem;
      letter-spacing: -0.02em;
    }}
    .nav-badge {{
      font-size: 0.6875rem;
      background: var(--accent-dim);
      color: var(--accent);
      border: 1px solid var(--accent);
      padding: 2px 8px;
      border-radius: var(--radius-full);
      font-weight: 600;
    }}
    .nav-links {{
      display: flex;
      align-items: center;
      gap: var(--space-4);
      font-size: 0.875rem;
    }}
    .nav-links a {{
      color: var(--text-muted);
      text-decoration: none;
      font-weight: 500;
      transition: color 0.15s ease;
    }}
    .nav-links a:hover {{
      color: var(--text);
    }}
    .theme-toggle {{
      background: var(--bg-surface);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 6px 12px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      font-size: 0.8125rem;
      font-family: inherit;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    /* How to Read This Page Strip */
    .read-strip {{
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border);
      font-size: 0.8125rem;
      color: var(--text-muted);
      padding: var(--space-2) var(--space-4);
    }}
    .read-strip-inner {{
      max-width: var(--max-width);
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: var(--space-2);
    }}
    .read-strip-inner strong {{
      color: var(--accent);
    }}

    /* Main Layout */
    main {{
      max-width: var(--max-width);
      width: 100%;
      margin: 0 auto;
      padding: var(--space-6) var(--space-4);
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: var(--space-8);
    }}

    section {{
      display: flex;
      flex-direction: column;
      gap: var(--space-4);
    }}

    .section-header {{
      display: flex;
      flex-direction: column;
      gap: var(--space-1);
      border-bottom: 1px solid var(--border);
      padding-bottom: var(--space-3);
    }}
    .section-title {{
      font-size: 1.5rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      color: var(--text);
    }}
    .section-takeaway {{
      font-size: 0.9375rem;
      color: var(--text-muted);
      max-width: 75ch;
      line-height: 1.4;
    }}

    /* Cards */
    .card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: var(--space-5);
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }}
    .card:hover {{
      border-color: rgba(204, 129, 97, 0.4);
    }}

    /* 1. HEADLINE & BIG NUMBERS */
    .hero-banner {{
      background: linear-gradient(145deg, var(--bg-card) 0%, var(--bg-surface) 100%);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: var(--space-6);
      display: flex;
      flex-direction: column;
      gap: var(--space-5);
    }}
    .hero-thesis {{
      font-size: 1.25rem;
      font-weight: 700;
      color: var(--text);
      line-height: 1.45;
      max-width: 75ch;
    }}
    .hero-thesis strong {{
      color: var(--accent);
    }}

    .stat-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: var(--space-4);
    }}
    .stat-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: var(--space-4);
      display: flex;
      flex-direction: column;
      gap: var(--space-2);
    }}
    .stat-label {{
      font-size: 0.75rem;
      font-family: var(--font-mono);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-dim);
    }}
    .stat-value {{
      font-size: 2.25rem;
      font-weight: 800;
      line-height: 1;
      letter-spacing: -0.03em;
      color: var(--accent);
    }}
    .stat-basis {{
      font-size: 0.75rem;
      color: var(--text-muted);
      line-height: 1.35;
    }}

    /* 2. PATTERNS (MAX 5 CARDS) */
    .pattern-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: var(--space-4);
    }}
    .pattern-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: var(--space-4);
      display: flex;
      flex-direction: column;
      gap: var(--space-2);
    }}
    .pattern-header {{
      display: flex;
      align-items: center;
      gap: var(--space-2);
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--accent);
      font-family: var(--font-mono);
    }}
    .pattern-title {{
      font-size: 1rem;
      font-weight: 700;
      color: var(--text);
      line-height: 1.3;
    }}
    .pattern-evidence {{
      font-size: 0.8125rem;
      color: var(--text-muted);
      line-height: 1.4;
    }}
    .pattern-so-what {{
      font-size: 0.8125rem;
      color: var(--text);
      background: var(--bg-surface);
      border-left: 3px solid var(--accent);
      padding: var(--space-2) var(--space-3);
      border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
      line-height: 1.35;
      margin-top: auto;
    }}
    .pattern-so-what strong {{
      color: var(--accent);
    }}

    /* Visual Distribution Charts (Offline SVG & CSS Bars) */
    .chart-container {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: var(--space-5);
      margin-top: var(--space-4);
    }}
    .chart-box {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: var(--space-5);
      display: flex;
      flex-direction: column;
      gap: var(--space-3);
    }}
    .chart-title {{
      font-size: 0.9375rem;
      font-weight: 700;
      color: var(--text);
    }}
    .chart-caption {{
      font-size: 0.75rem;
      color: var(--text-dim);
    }}
    .stacked-bar {{
      height: 28px;
      width: 100%;
      border-radius: var(--radius-sm);
      overflow: hidden;
      display: flex;
      background: var(--bg-surface);
      border: 1px solid var(--border);
    }}
    .bar-seg {{
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.6875rem;
      font-weight: 700;
      color: #040507;
      transition: width 0.3s ease;
    }}
    .bar-seg.ready {{ background: #22c55e; }}
    .bar-seg.caveat {{ background: #f59e0b; }}
    .bar-seg.gated {{ background: #f43f5e; }}
    .bar-seg.blocked {{ background: #94a3b8; }}

    .bar-seg.free {{ background: #22c55e; }}
    .bar-seg.paid {{ background: #38bdf8; }}
    .bar-seg.sales {{ background: #f43f5e; }}
    .bar-seg.approval {{ background: #f59e0b; }}
    .bar-seg.noapi {{ background: #94a3b8; }}

    .chart-legend {{
      display: flex;
      flex-wrap: wrap;
      gap: var(--space-3);
      font-size: 0.75rem;
      margin-top: var(--space-2);
    }}
    .legend-item {{
      display: flex;
      align-items: center;
      gap: 6px;
      color: var(--text-muted);
    }}
    .legend-dot {{
      width: 10px;
      height: 10px;
      border-radius: 2px;
    }}

    /* 3. AGENT PIPELINE FLOW DIAGRAM */
    .flow-wrapper {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: var(--space-5);
      overflow-x: auto;
    }}
    .flow-container {{
      display: flex;
      align-items: center;
      gap: var(--space-3);
      min-width: 760px;
      justify-content: space-between;
    }}
    .flow-node {{
      flex: 1;
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: var(--space-4);
      display: flex;
      flex-direction: column;
      gap: var(--space-2);
      position: relative;
    }}
    .flow-node.human-involved {{
      border-color: var(--accent);
      background: linear-gradient(180deg, var(--bg-surface) 0%, var(--accent-dim) 100%);
    }}
    .flow-step-tag {{
      font-size: 0.6875rem;
      font-family: var(--font-mono);
      font-weight: 700;
      color: var(--text-dim);
      text-transform: uppercase;
    }}
    .flow-title {{
      font-size: 0.875rem;
      font-weight: 700;
      color: var(--text);
    }}
    .flow-desc {{
      font-size: 0.75rem;
      color: var(--text-muted);
      line-height: 1.35;
    }}
    .flow-badge {{
      display: inline-block;
      font-size: 0.6875rem;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: var(--radius-sm);
      align-self: flex-start;
      margin-top: 4px;
    }}
    .flow-badge.auto {{
      background: var(--stone-dim);
      color: var(--text-muted);
    }}
    .flow-badge.human {{
      background: var(--accent);
      color: #040507;
    }}
    .flow-arrow {{
      color: var(--border-focus);
      font-size: 1.25rem;
      font-weight: 900;
      flex-shrink: 0;
    }}

    /* 4. VERIFICATION SECTION */
    .verification-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: var(--space-5);
    }}
    .table-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: var(--space-4);
      overflow-x: auto;
    }}
    table.compact-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.8125rem;
      text-align: left;
    }}
    table.compact-table th {{
      padding: var(--space-2) var(--space-3);
      border-bottom: 2px solid var(--border);
      color: var(--text-dim);
      font-family: var(--font-mono);
      font-size: 0.75rem;
      text-transform: uppercase;
    }}
    table.compact-table td {{
      padding: var(--space-2) var(--space-3);
      border-bottom: 1px solid var(--border);
      color: var(--text);
    }}
    .status-badge {{
      display: inline-block;
      padding: 2px 6px;
      border-radius: var(--radius-sm);
      font-size: 0.6875rem;
      font-weight: 700;
    }}
    .status-badge.hit {{
      background: var(--ready-bg);
      color: var(--ready-color);
    }}
    .status-badge.corrected {{
      background: var(--caveat-bg);
      color: var(--caveat-color);
    }}

    /* Defeated / Unresolved Box */
    .unresolved-box {{
      background: var(--bg-card);
      border: 1px solid var(--gated-color);
      border-left: 4px solid var(--gated-color);
      border-radius: var(--radius-md);
      padding: var(--space-5);
      display: flex;
      flex-direction: column;
      gap: var(--space-3);
    }}
    .unresolved-title {{
      font-size: 1rem;
      font-weight: 800;
      color: var(--text);
      display: flex;
      align-items: center;
      gap: var(--space-2);
    }}
    .unresolved-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: var(--space-3);
      margin-top: var(--space-2);
    }}
    .unresolved-item {{
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: var(--space-3);
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}
    .unresolved-app {{
      font-size: 0.8125rem;
      font-weight: 700;
      color: var(--gated-color);
    }}
    .unresolved-desc {{
      font-size: 0.75rem;
      color: var(--text-muted);
      line-height: 1.35;
    }}

    /* 5. 100-APP FINDINGS MATRIX */
    .matrix-controls {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: var(--space-2);
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: var(--space-3);
    }}
    .control-input, .control-select {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 6px 12px;
      border-radius: var(--radius-sm);
      font-size: 0.8125rem;
      font-family: inherit;
    }}
    .control-input:focus, .control-select:focus {{
      outline: none;
      border-color: var(--border-focus);
    }}
    .control-input {{
      flex: 1;
      min-width: 200px;
    }}

    .table-container {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      overflow-x: auto;
      max-height: 680px;
      position: relative;
    }}
    table.data-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.8125rem;
      text-align: left;
    }}
    table.data-table thead th {{
      position: sticky;
      top: 0;
      z-index: 10;
      background: var(--bg-surface);
      border-bottom: 2px solid var(--border);
      padding: var(--space-3);
      color: var(--text-dim);
      font-family: var(--font-mono);
      font-size: 0.6875rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      white-space: nowrap;
    }}
    table.data-table tbody tr {{
      border-bottom: 1px solid var(--border);
      transition: background 0.15s ease;
    }}
    table.data-table tbody tr:nth-child(even) {{
      background: rgba(223, 218, 212, 0.03);
    }}
    table.data-table tbody tr:hover {{
      background: var(--bg-card-hover);
    }}
    table.data-table td {{
      padding: var(--space-2) var(--space-3);
      vertical-align: top;
      color: var(--text);
    }}

    /* Sticky First Column for Tablet/Mobile */
    .col-sticky {{
      position: sticky;
      left: 0;
      background: inherit;
      z-index: 5;
    }}

    /* Colored Verdict Pills */
    .pill {{
      display: inline-block;
      padding: 2px 8px;
      border-radius: var(--radius-full);
      font-size: 0.6875rem;
      font-weight: 700;
      white-space: nowrap;
    }}
    .pill.ready {{
      background: var(--ready-bg);
      color: var(--ready-color);
      border: 1px solid var(--ready-color);
    }}
    .pill.caveats {{
      background: var(--caveat-bg);
      color: var(--caveat-color);
      border: 1px solid var(--caveat-color);
    }}
    .pill.gated {{
      background: var(--gated-bg);
      color: var(--gated-color);
      border: 1px solid var(--gated-color);
    }}
    .pill.blocked {{
      background: var(--blocked-bg);
      color: var(--blocked-color);
      border: 1px solid var(--blocked-color);
    }}

    /* Self-Serve Dots */
    .ss-indicator {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      font-size: 0.75rem;
      color: var(--text-muted);
    }}
    .ss-dot {{
      width: 7px;
      height: 7px;
      border-radius: 50%;
      flex-shrink: 0;
    }}
    .ss-dot.free {{ background: #22c55e; }}
    .ss-dot.paid {{ background: #38bdf8; }}
    .ss-dot.sales {{ background: #f43f5e; }}
    .ss-dot.approval {{ background: #f59e0b; }}
    .ss-dot.blocked {{ background: #94a3b8; }}

    /* MCP Pills */
    .mcp-pill {{
      display: inline-block;
      padding: 1px 6px;
      border-radius: var(--radius-sm);
      font-size: 0.6875rem;
      font-weight: 600;
    }}
    .mcp-pill.official {{
      background: rgba(34, 197, 94, 0.15);
      color: #22c55e;
    }}
    .mcp-pill.community {{
      background: rgba(56, 189, 248, 0.15);
      color: #38bdf8;
    }}
    .mcp-pill.greenfield {{
      background: var(--accent-dim);
      color: var(--accent);
      border: 1px solid var(--accent);
    }}

    /* Truncated Blocker Button */
    .blocker-truncate {{
      max-width: 180px;
      font-size: 0.75rem;
      color: var(--text-muted);
      cursor: pointer;
      display: block;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      background: none;
      border: none;
      text-align: left;
      font-family: inherit;
    }}
    .blocker-truncate:hover {{
      color: var(--text);
    }}
    .blocker-truncate.expanded {{
      white-space: normal;
      overflow: visible;
    }}

    /* 6. RUN IT + DOWNLOADS */
    .download-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: var(--space-4);
    }}
    .code-box {{
      background: #020304;
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: var(--space-4);
      font-family: var(--font-mono);
      font-size: 0.75rem;
      color: var(--text-muted);
      overflow-x: auto;
      line-height: 1.6;
    }}
    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: var(--space-2);
      padding: 8px 16px;
      border-radius: var(--radius-sm);
      font-size: 0.8125rem;
      font-weight: 600;
      text-decoration: none;
      cursor: pointer;
      border: 1px solid transparent;
      transition: all 0.15s ease;
    }}
    .btn-primary {{
      background: var(--accent);
      color: #040507;
    }}
    .btn-primary:hover {{
      background: var(--accent-hover);
    }}
    .btn-secondary {{
      background: var(--bg-surface);
      color: var(--text);
      border-color: var(--border);
    }}
    .btn-secondary:hover {{
      background: var(--bg-card-hover);
      border-color: var(--accent);
    }}

    /* Footer */
    footer {{
      background: var(--bg-surface);
      border-top: 1px solid var(--border);
      padding: var(--space-6) var(--space-4);
      text-align: center;
      font-size: 0.75rem;
      color: var(--text-dim);
    }}

    /* Utility */
    .font-mono {{ font-family: var(--font-mono); }}
    .text-xs {{ font-size: 0.75rem; }}
    .text-sm {{ font-size: 0.8125rem; }}
    .muted {{ color: var(--text-dim); }}

    /* Responsive adjustments */
    @media (max-width: 640px) {{
      .nav-links {{
        display: none;
      }}
      .hero-thesis {{
        font-size: 1.0625rem;
      }}
      .stat-value {{
        font-size: 1.75rem;
      }}
      table.data-table thead th, table.data-table td {{
        padding: 6px 8px;
      }}
    }}
  </style>
</head>
<body>
  <!-- Skip Link -->
  <a href="#matrix" class="skip-link">Skip to 100-App Table</a>

  <!-- Top Navigation -->
  <header class="sticky-nav">
    <div class="nav-container">
      <a href="#" class="nav-brand">
        <span>Composio</span>
        <span class="nav-badge">AI Product Ops</span>
      </a>
      <nav class="nav-links" aria-label="Page Sections">
        <a href="#headline">Headline</a>
        <a href="#patterns">Patterns</a>
        <a href="#agent">The Agent</a>
        <a href="#verification">Verification</a>
        <a href="#matrix">100-App Matrix</a>
        <a href="#run">Run & Download</a>
      </nav>
      <button class="theme-toggle" id="themeToggleBtn" aria-label="Toggle light or dark theme">
        <span id="themeIcon">☀</span> <span id="themeLabel">Light</span>
      </button>
    </div>
  </header>

  <!-- How to Read Strip -->
  <div class="read-strip">
    <div class="read-strip-inner">
      <span><strong>2-Minute Reviewer Guide:</strong> Review Headline Metrics &rarr; 5 Macro Patterns &rarr; Verification Progression (23% &rarr; 96%) &rarr; Interactive 100-App Table.</span>
      <span class="font-mono text-xs">100 Apps Audited &bull; Candidate: Adarsh Mishra</span>
    </div>
  </div>

  <main>
    <!-- SECTION A: HEADLINE & BIG NUMBERS -->
    <section id="headline">
      <div class="hero-banner">
        <div>
          <span class="nav-badge" style="margin-bottom: 8px; display: inline-block;">Take-Home Case Study</span>
          <h1 class="hero-thesis">
            <strong>{ready_pct}%</strong> of evaluated SaaS ecosystems are buildable for agentic toolkits today with self-serve access, while a multi-pass verification pipeline with human checks lifted extraction accuracy from <strong>{p1_strict}%</strong> to <strong>{p2_strict}%</strong>.
          </h1>
        </div>

        <div class="stat-grid">
          <div class="stat-card">
            <span class="stat-label">1. Ready for Toolkit Today</span>
            <div class="stat-value">{ready_pct}%</div>
            <span class="stat-basis"><strong>{ready_count} of {total} apps</strong> have documented public APIs and self-serve access ({free_ss_count} free tier/trial, {paid_ss_count} paid plan).</span>
          </div>

          <div class="stat-card">
            <span class="stat-label">2. Free Self-Serve vs Gated</span>
            <div class="stat-value">{free_ss_pct}% / {total_gated_pct}%</div>
            <span class="stat-basis"><strong>{free_ss_count} Free Self-Serve</strong> vs <strong>{total_gated_count} Total Gated</strong> (9 enterprise sales walls, 5 platform app reviews, 1 blocked).</span>
          </div>

          <div class="stat-card">
            <span class="stat-label">3. Composio MCP Greenfield</span>
            <div class="stat-value">{greenfield_pct}%</div>
            <span class="stat-basis"><strong>{greenfield_count} of {total} apps</strong> have zero existing official or community MCP servers—uncontested distribution wins.</span>
          </div>

          <div class="stat-card">
            <span class="stat-label">4. Verified Record Accuracy</span>
            <div class="stat-value">{p1_strict}% &rarr; {p2_strict}%</div>
            <span class="stat-basis">Lifted across all fields (23/100 to 96/100) via automated HTTP link probes and human review. <strong>{residual_count} residual caveats</strong> disclosed.</span>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION B: PATTERNS (MAX 5 CARDS) -->
    <section id="patterns">
      <div class="section-header">
        <h2 class="section-title">Macro Patterns & Strategic Clustering</h2>
        <p class="section-takeaway">5 high-impact architectural patterns across auth, gating, and developer surfaces that dictate Composio's toolkit roadmap.</p>
      </div>

      <div class="pattern-grid">
        <!-- Card 1 -->
        <div class="pattern-card">
          <div class="pattern-header">PATTERN 01</div>
          <h3 class="pattern-title">Dual-Track Auth Dominance</h3>
          <p class="pattern-evidence"><strong>OAuth2 for Multi-Tenant Enterprise vs Bearer Keys for Dev/Infra:</strong> 58% of apps use Bearer API keys, while 25% mandate OAuth2 with granular scopes.</p>
          <div class="pattern-so-what">
            <strong>So what for Composio:</strong> Managed auth handles OAuth refresh tokens, eliminating user authentication friction across CRM and Marketing stacks.
          </div>
        </div>

        <!-- Card 2 -->
        <div class="pattern-card">
          <div class="pattern-header">PATTERN 02</div>
          <h3 class="pattern-title">The 15% Hard-Gating Landscape</h3>
          <p class="pattern-evidence"><strong>Only 15 Platforms Gate Developer Self-Serve Access:</strong> 9 enterprise sales gates, 5 manual app review processes, and 1 non-API application.</p>
          <div class="pattern-so-what">
            <strong>So what for Composio:</strong> Prioritize automated tool generation for the 81% self-serve apps; route gated enterprise tools to dedicated BD partnership tracks.
          </div>
        </div>

        <!-- Card 3 -->
        <div class="pattern-card">
          <div class="pattern-header">PATTERN 03</div>
          <h3 class="pattern-title">Review Gates as Moats</h3>
          <p class="pattern-evidence"><strong>Ad Networks & Marketplaces Mandate Compliance Audits:</strong> Google Ads, Meta Ads, and Amazon SP-API enforce DPP review and developer token approvals.</p>
          <div class="pattern-so-what">
            <strong>So what for Composio:</strong> Submit umbrella verified partner apps so end-users connect instantly without waiting weeks for individual platform review approvals.
          </div>
        </div>

        <!-- Card 4 -->
        <div class="pattern-card">
          <div class="pattern-header">PATTERN 04</div>
          <h3 class="pattern-title">The 42% MCP Greenfield</h3>
          <p class="pattern-evidence"><strong>42 Apps Have Zero Official or Community MCP Servers:</strong> High-demand CRM, Support, and Marketing apps (Front, Help Scout, Close) lack canonical MCP implementations.</p>
          <div class="pattern-so-what">
            <strong>So what for Composio:</strong> Fast-tracking canonical Composio MCP servers in these categories captures uncontested developer market share.
          </div>
        </div>

        <!-- Card 5 -->
        <div class="pattern-card">
          <div class="pattern-header">PATTERN 05</div>
          <h3 class="pattern-title">Local CLI & Subprocess Execution</h3>
          <p class="pattern-evidence"><strong>Specialized OSINT & Visual Tools Require Local Runtime:</strong> Sherlock and Mermaid CLI execute as local subprocesses and scripts, not remote cloud APIs.</p>
          <div class="pattern-so-what">
            <strong>So what for Composio:</strong> Toolkit architecture should support sandboxed local CLI executors alongside cloud HTTP tool runners.
          </div>
        </div>
      </div>

      <!-- Offline CSS/SVG Distribution Charts -->
      <div class="chart-container">
        <div class="chart-box">
          <div class="chart-title">Buildability Verdicts Across 100 Apps</div>
          <div class="chart-caption">Distribution of ready, caveat-bound, gated, and blocked integrations.</div>
          <div class="stacked-bar" role="img" aria-label="Buildability Verdict Bar: 81% Ready, 10% Caveats, 8% Gated, 1% Blocked">
            <div class="bar-seg ready" style="width: 81%;">{ready_pct}%</div>
            <div class="bar-seg caveat" style="width: 10%;">{feasible_pct}%</div>
            <div class="bar-seg gated" style="width: 8%;">{gated_pct}%</div>
            <div class="bar-seg blocked" style="width: 1%;">{blocked_pct}%</div>
          </div>
          <div class="chart-legend">
            <div class="legend-item"><span class="legend-dot" style="background:#22c55e;"></span> Ready Today ({ready_count})</div>
            <div class="legend-item"><span class="legend-dot" style="background:#f59e0b;"></span> Caveats ({feasible_count})</div>
            <div class="legend-item"><span class="legend-dot" style="background:#f43f5e;"></span> Gated ({gated_count})</div>
            <div class="legend-item"><span class="legend-dot" style="background:#94a3b8;"></span> Blocked ({blocked_count})</div>
          </div>
        </div>

        <div class="chart-box">
          <div class="chart-title">Self-Serve vs Gating Breakdown</div>
          <div class="chart-caption">Developer accessibility: free self-serve, paid plans, sales walls, and review gates.</div>
          <div class="stacked-bar" role="img" aria-label="Gating Distribution Bar: 74% Free Self-Serve, 11% Paid, 9% Sales Wall, 5% Approval, 1% No API">
            <div class="bar-seg free" style="width: 74%;">{free_ss_pct}%</div>
            <div class="bar-seg paid" style="width: 11%;">{paid_ss_pct}%</div>
            <div class="bar-seg sales" style="width: 9%;">9%</div>
            <div class="bar-seg approval" style="width: 5%;">5%</div>
            <div class="bar-seg noapi" style="width: 1%;">1%</div>
          </div>
          <div class="chart-legend">
            <div class="legend-item"><span class="legend-dot" style="background:#22c55e;"></span> Free Tier/Trial ({free_ss_count})</div>
            <div class="legend-item"><span class="legend-dot" style="background:#38bdf8;"></span> Paid Plan ({paid_ss_count})</div>
            <div class="legend-item"><span class="legend-dot" style="background:#f43f5e;"></span> Sales Wall (9)</div>
            <div class="legend-item"><span class="legend-dot" style="background:#f59e0b;"></span> Approval Gate (5)</div>
            <div class="legend-item"><span class="legend-dot" style="background:#94a3b8;"></span> No API (1)</div>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION C: THE AGENT & HUMAN-IN-THE-LOOP -->
    <section id="agent">
      <div class="section-header">
        <h2 class="section-title">The Research Pipeline & Human-in-the-Loop</h2>
        <p class="section-takeaway">Left-to-right verification pipeline combining automated extraction, link probing, and human verification where automated agents fail.</p>
      </div>

      <div class="flow-wrapper">
        <div class="flow-container">
          <!-- Step 1 -->
          <div class="flow-node">
            <span class="flow-step-tag">Step 1</span>
            <div class="flow-title">Notion App Input</div>
            <p class="flow-desc">100 SaaS apps across 10 categories ingested from the official brief.</p>
            <span class="flow-badge auto">Automated</span>
          </div>

          <div class="flow-arrow">&rarr;</div>

          <!-- Step 2 -->
          <div class="flow-node">
            <span class="flow-step-tag">Step 2</span>
            <div class="flow-title">Pass 1: LLM Extraction</div>
            <p class="flow-desc">Naive extraction. High verdict recall (78%) but missed hidden sales gates and deprecated auth (23% strict).</p>
            <span class="flow-badge auto">Automated (23% Strict)</span>
          </div>

          <div class="flow-arrow">&rarr;</div>

          <!-- Step 3 -->
          <div class="flow-node">
            <span class="flow-step-tag">Step 3</span>
            <div class="flow-title">Automated Verification</div>
            <p class="flow-desc">HTTP link probes with browser User-Agents, MCP registry queries, and Pydantic schema validation.</p>
            <span class="flow-badge auto">Automated Tooling</span>
          </div>

          <div class="flow-arrow">&rarr;</div>

          <!-- Step 4 -->
          <div class="flow-node human-involved">
            <span class="flow-step-tag" style="color: var(--accent);">Step 4</span>
            <div class="flow-title">Human-in-the-Loop</div>
            <p class="flow-desc">Resolved Cloudflare 403s, caught enterprise sales pricing walls, verified session cookie reverse engineering.</p>
            <span class="flow-badge human">Human Needed Here</span>
          </div>

          <div class="flow-arrow">&rarr;</div>

          <!-- Step 5 -->
          <div class="flow-node">
            <span class="flow-step-tag">Step 5</span>
            <div class="flow-title">Curated Dataset</div>
            <p class="flow-desc">100 verified records, 96% strict accuracy, and 4 documented residual caveats.</p>
            <span class="flow-badge auto">Pass 2: 96% Strict</span>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION D: VERIFICATION & ACCURACY PROGRESSION -->
    <section id="verification">
      <div class="section-header">
        <h2 class="section-title">Accuracy Progression & Verification Proof</h2>
        <p class="section-takeaway">Measurable accuracy progression from naive Pass 1 extraction to verified Pass 2 ground truth across full dataset and targeted samples.</p>
      </div>

      <div class="verification-grid">
        <!-- Pass 1 vs Pass 2 Table -->
        <div class="table-card">
          <div style="font-weight: 700; margin-bottom: 8px;">Per-Field Accuracy Lift (N=100)</div>
          <table class="compact-table">
            <thead>
              <tr>
                <th>Field Dimension</th>
                <th>Pass 1</th>
                <th>Pass 2</th>
                <th>Delta</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Buildability Verdict</td>
                <td class="font-mono">78 / 100 (78%)</td>
                <td class="font-mono" style="color:var(--ready-color);">98 / 100 (98%)</td>
                <td class="font-mono" style="color:var(--accent);">+20%</td>
              </tr>
              <tr>
                <td>Self-Serve Status</td>
                <td class="font-mono">71 / 100 (71%)</td>
                <td class="font-mono" style="color:var(--ready-color);">98 / 100 (98%)</td>
                <td class="font-mono" style="color:var(--accent);">+27%</td>
              </tr>
              <tr>
                <td>Primary Auth Method</td>
                <td class="font-mono">31 / 100 (31%)</td>
                <td class="font-mono" style="color:var(--ready-color);">98 / 100 (98%)</td>
                <td class="font-mono" style="color:var(--accent);">+67%</td>
              </tr>
              <tr style="background: var(--bg-surface); font-weight: 700;">
                <td>Strict Record Match (All Fields)</td>
                <td class="font-mono">23 / 100 ({p1_strict}%)</td>
                <td class="font-mono" style="color:var(--ready-color);">96 / 100 ({p2_strict}%)</td>
                <td class="font-mono" style="color:var(--accent);">+73%</td>
              </tr>
            </tbody>
          </table>
          <p class="text-xs muted" style="margin-top: 8px;">*Pass 1 failed strictly because models assumed static API keys and missed hidden enterprise sales gates.</p>
        </div>

        <!-- Hits & Misses Table -->
        <div class="table-card">
          <div style="font-weight: 700; margin-bottom: 8px;">Audit Sample: Hits & Corrected Misses</div>
          <table class="compact-table">
            <thead>
              <tr>
                <th>App</th>
                <th>Pass 1 Claim</th>
                <th>Pass 2 Ground Truth</th>
                <th>Result</th>
                <th>Reason</th>
              </tr>
            </thead>
            <tbody>
              {sample_rows_html}
            </tbody>
          </table>
        </div>
      </div>

      <!-- WHERE THE AGENT WAS STILL WRONG OR DEFEATED -->
      <div class="unresolved-box">
        <div class="unresolved-title">
          <span>&#9888;</span>
          <span>Where the Agent Was Still Wrong or Defeated ({residual_count} Residual Caveats / {residual_pct}%)</span>
        </div>
        <p class="text-xs muted">
          In strict compliance with assignment evaluation rules, we disclose the 4 platforms that defeated automated extraction or carry unresolved integration fragility:
        </p>
        <div class="unresolved-grid">
          <div class="unresolved-item">
            <span class="unresolved-app">#92 Otter AI &bull; AI Media</span>
            <p class="unresolved-desc"><strong>Unofficial Session Token Fragility:</strong> Has no documented public developer REST API. Community MCP implementations reverse-engineer user session cookies (<code>auth_token</code>), which break on UI logout or CSRF token refresh.</p>
          </div>
          <div class="unresolved-item">
            <span class="unresolved-app">#91 NotebookLM &bull; AI Media</span>
            <p class="unresolved-desc"><strong>Consumer vs Enterprise Separation:</strong> The consumer application has no public API. Programmatic integration requires an enterprise Google Cloud Discovery Engine license with GCP IAM credentials.</p>
          </div>
          <div class="unresolved-item">
            <span class="unresolved-app">#50 Fanbasis &bull; Ecommerce</span>
            <p class="unresolved-desc"><strong>Zero Public Endpoints:</strong> The only platform among 100 with no developer portal, documentation, or public API. Agent toolkit integration requires browser-use automation.</p>
          </div>
          <div class="unresolved-item">
            <span class="unresolved-app">#90 PitchBook &bull; Fintech</span>
            <p class="unresolved-desc"><strong>Cloudflare WAF Shield & Sales Gate:</strong> Shields developer portal behind Cloudflare Enterprise WAF (HTTP 403 on CLI requests); requires an enterprise sales agreement.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION E: 100-APP FINDINGS MATRIX -->
    <section id="matrix">
      <div class="section-header">
        <h2 class="section-title">100-App Research & Buildability Matrix</h2>
        <p class="section-takeaway">Full interactive dataset of 100 SaaS applications. Search, filter by category or verdict, inspect authentication specs, and access official documentation.</p>
      </div>

      <!-- Filter Controls -->
      <div class="matrix-controls">
        <input type="text" id="searchInput" class="control-input" placeholder="Search app name, auth protocol, blocker, notes..." aria-label="Search apps">
        
        <select id="categoryFilter" class="control-select" aria-label="Filter by category">
          <option value="ALL">All 10 Categories</option>
        </select>

        <select id="verdictFilter" class="control-select" aria-label="Filter by verdict">
          <option value="ALL">All Verdicts</option>
          <option value="Ready Today">Ready Today ({ready_count})</option>
          <option value="Feasible with Caveats">Feasible with Caveats ({feasible_count})</option>
          <option value="Gated / Partner Required">Gated / Partner ({gated_count})</option>
          <option value="Blocked (No API)">Blocked ({blocked_count})</option>
        </select>

        <select id="selfServeFilter" class="control-select" aria-label="Filter by self-serve status">
          <option value="ALL">All Access Types</option>
          <option value="Free">Free Tier / Trial ({free_ss_count})</option>
          <option value="Paid">Paid Plan ({paid_ss_count})</option>
          <option value="Gated">Gated / Non-Self-Serve ({total_gated_count})</option>
        </select>
        
        <span id="rowCount" class="font-mono text-xs muted" style="margin-left: auto;">Showing 100 of 100 apps</span>
      </div>

      <!-- Data Table -->
      <div class="table-container">
        <table class="data-table" aria-label="100-App Research Findings">
          <thead>
            <tr>
              <th scope="col" style="width: 44px;">#</th>
              <th scope="col" class="col-sticky" style="width: 140px;">App</th>
              <th scope="col" style="width: 130px;">Category</th>
              <th scope="col" style="width: 130px;">Verdict</th>
              <th scope="col" style="width: 150px;">Self-Serve Status</th>
              <th scope="col" style="width: 150px;">Auth Method(s)</th>
              <th scope="col" style="width: 130px;">MCP Status</th>
              <th scope="col" style="width: 160px;">Blocker</th>
              <th scope="col" style="min-width: 200px;">Notes & Caveats</th>
              <th scope="col" style="width: 70px;">Docs</th>
            </tr>
          </thead>
          <tbody id="matrixTableBody">
            <!-- Dynamically populated via JS -->
          </tbody>
        </table>
      </div>
    </section>

    <!-- SECTION F: RUN IT YOURSELF & DOWNLOADS -->
    <section id="run">
      <div class="section-header">
        <h2 class="section-title">Run It Yourself & Dataset Downloads</h2>
        <p class="section-takeaway">Reproduce the verification pipeline locally from the open-source repository or download raw JSON/CSV datasets.</p>
      </div>

      <div class="download-grid">
        <div class="card" style="display:flex; flex-direction:column; gap: var(--space-3);">
          <div style="font-weight:700;">Execute Verification Pipeline Locally</div>
          <div class="code-box">
# 1. Clone repository<br>
git clone https://github.com/Adarshhic/Product---Intern-Task.git<br>
cd Product---Intern-Task<br><br>
# 2. Run unit tests<br>
python -m unittest discover tests<br><br>
# 3. Run live HTTP verification probe on sample<br>
python run.py --sample 10<br><br>
# 4. Run full verification and pattern analysis<br>
python run.py --all
          </div>
        </div>

        <div class="card" style="display:flex; flex-direction:column; justify-content:space-between; gap: var(--space-3);">
          <div style="display:flex; flex-direction:column; gap: var(--space-2);">
            <div style="font-weight:700;">Raw Data Artifacts for Agents & Humans</div>
            <p class="text-xs muted">
              All findings are structured according to the take-home specification and exported in standard formats:
            </p>
            <ul class="text-xs muted" style="list-style-type: none; display: flex; flex-direction: column; gap: 6px; margin-top: 4px;">
              <li>&bull; <strong>100 Apps Audited:</strong> 10 categories &times; 10 apps</li>
              <li>&bull; <strong>Evidence URLs:</strong> 100% verified working documentation links</li>
              <li>&bull; <strong>Schema:</strong> 11 standardized attributes per application</li>
            </ul>
          </div>

          <div style="display:flex; gap: var(--space-2); flex-wrap:wrap; margin-top: var(--space-3);">
            <a href="data/apps_research_dataset.json" download="apps_research_dataset.json" class="btn btn-primary" aria-label="Download JSON Dataset">
              &darr; Download JSON
            </a>
            <a href="data/apps_research_dataset.csv" download="apps_research_dataset.csv" class="btn btn-secondary" aria-label="Download CSV Dataset">
              &darr; Download CSV
            </a>
            <a href="https://github.com/Adarshhic/Product---Intern-Task" target="_blank" rel="noopener noreferrer" class="btn btn-secondary" aria-label="View GitHub Repository">
              GitHub Repo &rarr;
            </a>
          </div>
        </div>
      </div>
    </section>
  </main>

  <footer>
    <div style="max-width: var(--max-width); margin: 0 auto; display:flex; flex-direction:column; gap: 8px;">
      <div>Composio AI Product Ops Intern Take-Home &bull; Candidate: Adarsh Mishra &bull; November 2026</div>
      <div class="font-mono text-xs">Offline-first build: Zero external CDN dependencies &bull; System Typography &bull; Accessible Semantic HTML</div>
    </div>
  </footer>

  <!-- Raw Dataset Script Block for Agents & JS Table Hydration -->
  <script type="application/json" id="dataset">
{dataset_json_str}
  </script>

  <script>
    (function() {{
      const dataset = JSON.parse(document.getElementById('dataset').textContent);
      const tbody = document.getElementById('matrixTableBody');
      const searchInput = document.getElementById('searchInput');
      const categoryFilter = document.getElementById('categoryFilter');
      const verdictFilter = document.getElementById('verdictFilter');
      const selfServeFilter = document.getElementById('selfServeFilter');
      const rowCount = document.getElementById('rowCount');

      // Populate Category Filter options
      const categories = [...new Set(dataset.map(a => a.category))].sort();
      categories.forEach(cat => {{
        const opt = document.createElement('option');
        opt.value = cat;
        opt.textContent = cat;
        categoryFilter.appendChild(opt);
      }});

      function getPillClass(verdict) {{
        if (verdict === 'Ready Today') return 'ready';
        if (verdict === 'Feasible with Caveats') return 'caveats';
        if (verdict === 'Gated / Partner Required') return 'gated';
        return 'blocked';
      }}

      function getSelfServeDot(status) {{
        if (status.includes('Free Tier') || status.includes('Free Trial')) return 'free';
        if (status.includes('Paid Plan')) return 'paid';
        if (status.includes('Sales') || status.includes('Partner')) return 'sales';
        if (status.includes('Admin') || status.includes('Approval')) return 'approval';
        return 'blocked';
      }}

      function getMcpClass(mcp) {{
        if (mcp.includes('Official')) return 'official';
        if (mcp.includes('Community')) return 'community';
        return 'greenfield';
      }}

      function renderTable() {{
        const q = searchInput.value.toLowerCase().trim();
        const cat = categoryFilter.value;
        const verd = verdictFilter.value;
        const ss = selfServeFilter.value;

        const filtered = dataset.filter(a => {{
          const matchQ = !q || 
            a.name.toLowerCase().includes(q) ||
            a.category.toLowerCase().includes(q) ||
            (a.primary_auth && a.primary_auth.toLowerCase().includes(q)) ||
            (a.main_blocker && a.main_blocker.toLowerCase().includes(q)) ||
            (a.notes && a.notes.toLowerCase().includes(q));

          const matchCat = cat === 'ALL' || a.category === cat;
          const matchVerd = verd === 'ALL' || a.buildability_verdict === verd;
          
          let matchSS = true;
          if (ss === 'Free') matchSS = a.self_serve_status.includes('Free Tier') || a.self_serve_status.includes('Free Trial');
          else if (ss === 'Paid') matchSS = a.self_serve_status.includes('Paid Plan');
          else if (ss === 'Gated') matchSS = !a.self_serve_status.includes('Self-Serve');

          return matchQ && matchCat && matchVerd && matchSS;
        }});

        tbody.innerHTML = '';
        filtered.forEach(a => {{
          const tr = document.createElement('tr');

          const pillCls = getPillClass(a.buildability_verdict);
          const ssDotCls = getSelfServeDot(a.self_serve_status);
          const mcpCls = getMcpClass(a.mcp_status);

          const authText = Array.isArray(a.auth_methods) ? a.auth_methods.join(', ') : (a.primary_auth || 'API Key');
          const blockerText = (a.main_blocker && a.main_blocker !== 'None') ? a.main_blocker : 'None';
          const notesText = a.notes || 'Self-serve credentials and documented public API available.';

          tr.innerHTML = `
            <td class="font-mono text-xs muted">${{a.id}}</td>
            <td class="col-sticky"><strong>${{a.name}}</strong></td>
            <td class="text-xs muted">${{a.category}}</td>
            <td><span class="pill ${{pillCls}}">${{a.buildability_verdict}}</span></td>
            <td>
              <span class="ss-indicator">
                <span class="ss-dot ${{ssDotCls}}"></span>
                <span>${{a.self_serve_status}}</span>
              </span>
            </td>
            <td class="font-mono text-xs">${{authText}}</td>
            <td><span class="mcp-pill ${{mcpCls}}">${{a.mcp_status}}</span></td>
            <td>
              <button type="button" class="blocker-truncate" title="Click to expand blocker detail">
                ${{blockerText}}
              </button>
            </td>
            <td class="text-xs muted">${{notesText}}</td>
            <td class="text-xs font-mono">
              <a href="${{a.evidence_url}}" target="_blank" rel="noopener noreferrer" style="color:var(--accent); text-decoration:none;" title="${{a.evidence_url}}">Docs &rarr;</a>
            </td>
          `;
          tbody.appendChild(tr);
        }});

        // Attach expand toggle for truncated blockers
        tbody.querySelectorAll('.blocker-truncate').forEach(btn => {{
          btn.addEventListener('click', () => {{
            btn.classList.toggle('expanded');
          }});
        }});

        rowCount.textContent = `Showing ${{filtered.length}} of ${{dataset.length}} apps`;
      }}

      searchInput.addEventListener('input', renderTable);
      categoryFilter.addEventListener('change', renderTable);
      verdictFilter.addEventListener('change', renderTable);
      selfServeFilter.addEventListener('change', renderTable);

      renderTable();

      // Theme Toggle Logic
      const themeToggleBtn = document.getElementById('themeToggleBtn');
      const themeIcon = document.getElementById('themeIcon');
      const themeLabel = document.getElementById('themeLabel');

      function setTheme(theme) {{
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('composio-theme', theme);
        if (theme === 'light') {{
          themeIcon.textContent = '🌙';
          themeLabel.textContent = 'Dark';
        }} else {{
          themeIcon.textContent = '☀';
          themeLabel.textContent = 'Light';
        }}
      }}

      const savedTheme = localStorage.getItem('composio-theme') || 'dark';
      setTheme(savedTheme);

      themeToggleBtn.addEventListener('click', () => {{
        const currentTheme = document.documentElement.getAttribute('data-theme');
        setTheme(currentTheme === 'dark' ? 'light' : 'dark');
      }});
    }})();
  </script>
</body>
</html>
"""

    out_file = BASE_DIR / "web" / "index.html"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    root_file = BASE_DIR / "index.html"
    with open(root_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Case study HTML generated at {out_file} and {root_file} ({len(html_content)} bytes)")

if __name__ == "__main__":
    generate_html()
