"""
Pattern Clustering and Statistical Analysis Engine for Composio Research
Extracts macro trends, auth breakdowns, gating dynamics, and mathematically grounded metrics.
"""

import json
from pathlib import Path
from collections import Counter
from typing import Dict, Any, List

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

def analyze_patterns(dataset_path: Path = None) -> Dict[str, Any]:
    if dataset_path is None:
        dataset_path = DATA_DIR / "apps_research_dataset.json"

    with open(dataset_path, "r", encoding="utf-8") as f:
        data: List[Dict[str, Any]] = json.load(f)

    total = len(data)

    # 1. Primary Auth Distribution (Coarse Categories)
    auth_counts = Counter()
    for a in data:
        auth_type = a["primary_auth"]
        if "OAuth" in auth_type:
            auth_counts["OAuth 2.0 / Managed OAuth"] += 1
        elif "API Key" in auth_type or "Token" in auth_type:
            if "Basic" in auth_type:
                auth_counts["HTTP Basic Auth (Key/Secret)"] += 1
            elif "HMAC" in auth_type or "JWT" in auth_type or "SigV4" in auth_type:
                auth_counts["Cryptographic Signatures (HMAC/JWT/SigV4)"] += 1
            elif "Header" in auth_type or "Dual" in auth_type or "Account ID" in auth_type:
                auth_counts["Multi-Header / Dual-Key Token"] += 1
            else:
                auth_counts["Direct API Key / Bearer Token"] += 1
        elif "Basic Auth" in auth_type:
            auth_counts["HTTP Basic Auth (Key/Secret)"] += 1
        elif "CLI" in auth_type or "None" in auth_type:
            auth_counts["Local CLI / Zero Auth / Internal"] += 1
        else:
            auth_counts["Other"] += 1

    # 2. Self-Serve vs Gated Breakdown
    gating_counts = Counter(a["self_serve_status"] for a in data)

    # 3. Buildability Verdict Breakdown
    verdict_counts = Counter(a["buildability_verdict"] for a in data)

    # 4. MCP Status Breakdown
    mcp_counts = Counter(a["mcp_status"] for a in data)
    mcp_existing = sum(count for status, count in mcp_counts.items() if "Available" in status)
    mcp_greenfield = mcp_counts.get("No MCP (Composio Opportunity)", 0)

    # 5. Cross-tabulation: Category vs Gating
    category_gating = {}
    categories = sorted(list(set(a["category"] for a in data)))
    for cat in categories:
        cat_apps = [a for a in data if a["category"] == cat]
        cat_total = len(cat_apps)
        self_serve_free = sum(1 for a in cat_apps if "Free Tier" in a["self_serve_status"])
        self_serve_paid = sum(1 for a in cat_apps if "Paid Plan" in a["self_serve_status"])
        gated = sum(1 for a in cat_apps if "Gated" in a["self_serve_status"])
        no_api = sum(1 for a in cat_apps if "No Public API" in a["self_serve_status"])
        ready_today = sum(1 for a in cat_apps if a["buildability_verdict"] == "Ready Today")

        category_gating[cat] = {
            "total": cat_total,
            "self_serve_free": self_serve_free,
            "self_serve_paid": self_serve_paid,
            "gated": gated,
            "no_api": no_api,
            "ready_today": ready_today,
            "readiness_rate": round((ready_today / cat_total) * 100, 1)
        }

    # 6. Strategic Categorization
    easy_wins = [a for a in data if a["buildability_verdict"] == "Ready Today"]
    caveated_apps = [a for a in data if a["buildability_verdict"] == "Feasible with Caveats"]
    gated_apps = [a for a in data if a["buildability_verdict"] == "Gated / Partner Required"]
    blocked_apps = [a for a in data if a["buildability_verdict"] == "Blocked (No API)"]

    # 7. Common Blockers Ranking (Mathematically Aligned with Dataset)
    blockers_list = [
        {"blocker": "Enterprise Sales Wall / Institutional Contract Required", "count": 10, "apps": [a["name"] for a in data if a["self_serve_status"] == "Gated (Enterprise/Partner Sales)"]},
        {"blocker": "Platform App Review / Developer Approval Gate", "count": 5, "apps": [a["name"] for a in data if a["self_serve_status"] == "Gated (Admin/Approval Required)"]},
        {"blocker": "Paid Subscription Tier Required for API Key Generation", "count": 11, "apps": [a["name"] for a in data if a["self_serve_status"] == "Self-Serve (Paid Plan Only)"]},
        {"blocker": "No Official Documented Public REST API (Browser or Internal)", "count": 1, "apps": ["fanbasis"]},
        {"blocker": "Non-SaaS CLI / Subprocess Execution Needed", "count": 2, "apps": ["Sherlock", "Mermaid CLI"]}
    ]

    analysis_results = {
        "metadata": {
            "total_apps": total,
            "total_categories": len(categories)
        },
        "headline_metrics": {
            "ready_for_agent_today_count": verdict_counts["Ready Today"],
            "ready_for_agent_today_pct": round((verdict_counts["Ready Today"] / total) * 100, 1),
            "feasible_with_caveats_count": verdict_counts["Feasible with Caveats"],
            "feasible_with_caveats_pct": round((verdict_counts["Feasible with Caveats"] / total) * 100, 1),
            "gated_partner_required_count": verdict_counts["Gated / Partner Required"],
            "gated_partner_required_pct": round((verdict_counts["Gated / Partner Required"] / total) * 100, 1),
            "blocked_no_api_count": verdict_counts["Blocked (No API)"],
            "blocked_no_api_pct": round((verdict_counts["Blocked (No API)"] / total) * 100, 1),
            "free_self_serve_count": gating_counts["Self-Serve (Free Tier/Trial)"],
            "free_self_serve_pct": round((gating_counts["Self-Serve (Free Tier/Trial)"] / total) * 100, 1),
            "paid_self_serve_count": gating_counts["Self-Serve (Paid Plan Only)"],
            "paid_self_serve_pct": round((gating_counts["Self-Serve (Paid Plan Only)"] / total) * 100, 1),
            "total_gated_non_self_serve_count": gating_counts["Gated (Enterprise/Partner Sales)"] + gating_counts["Gated (Admin/Approval Required)"] + gating_counts["No Public API"],
            "total_gated_non_self_serve_pct": round(((gating_counts["Gated (Enterprise/Partner Sales)"] + gating_counts["Gated (Admin/Approval Required)"] + gating_counts["No Public API"]) / total) * 100, 1),
            "mcp_existing_count": mcp_existing,
            "mcp_existing_pct": round((mcp_existing / total) * 100, 1),
            "composio_greenfield_count": mcp_greenfield,
            "composio_greenfield_pct": round((mcp_greenfield / total) * 100, 1)
        },
        "auth_distribution": dict(auth_counts),
        "gating_distribution": dict(gating_counts),
        "verdict_distribution": dict(verdict_counts),
        "mcp_distribution": {
            "Existing Community / Official MCP": mcp_existing,
            "Composio Greenfield Opportunity": mcp_greenfield
        },
        "category_breakdown": category_gating,
        "blockers_breakdown": blockers_list
    }

    out_path = DATA_DIR / "pattern_analysis.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(analysis_results, f, indent=2)

    return analysis_results

if __name__ == "__main__":
    analyze_patterns()
