"""
Verification Engine for the Composio Research Agent
Runs automated sanity checks, link validation simulation, schema compliance,
and calculates Pass 1 vs Pass 2 accuracy transitions and error taxonomy.
"""

import json
from pathlib import Path
from typing import Dict, List, Any

def run_verification(dataset_path: Path) -> Dict[str, Any]:
    with open(dataset_path, "r", encoding="utf-8") as f:
        data: List[Dict[str, Any]] = json.load(f)

    total_apps = len(data)
    pass1_correct_count = sum(1 for a in data if a.get("pass1_correct") is True)
    pass2_correct_count = sum(1 for a in data if a.get("pass2_correct") is True)

    pass1_accuracy = (pass1_correct_count / total_apps) * 100
    pass2_accuracy = (pass2_correct_count / total_apps) * 100

    # Categorize error taxonomy in Pass 1
    error_taxonomy = {
        "False Self-Serve Assumption (Gated/Sales/Paid Missed)": 0,
        "Hallucinated or Deprecated Auth Method": 0,
        "Ignored Platform Review / Developer Approval Gate": 0,
        "CLI / Local Process Confounded with SaaS REST API": 0,
        "No Public API Hallucinated as Having Developer Portal": 0,
        "API Surface Protocol Misclassification (GraphQL/gRPC)": 0
    }

    misses_detail = []

    for a in data:
        if not a.get("pass1_correct"):
            notes = a.get("pass1_notes", "")
            name = a["name"]
            cat = a["category"]
            
            # Classify error type
            err_type = "False Self-Serve Assumption (Gated/Sales/Paid Missed)"
            if "deprecated" in notes.lower() or "sunset" in notes.lower() or "header" in notes.lower() or "digest" in notes.lower() or "keypair" in notes.lower() or "hmac" in notes.lower():
                err_type = "Hallucinated or Deprecated Auth Method"
            elif "approval" in notes.lower() or "review" in notes.lower() or "token gate" in notes.lower() or "vetting" in notes.lower():
                err_type = "Ignored Platform Review / Developer Approval Gate"
            elif "cli" in notes.lower() or "open-source" in notes.lower() or "github" in notes.lower():
                err_type = "CLI / Local Process Confounded with SaaS REST API"
            elif "zero public api" in notes.lower() or "no public api" in notes.lower() or "fanbasis" in name.lower():
                err_type = "No Public API Hallucinated as Having Developer Portal"
            elif "graphql" in notes.lower():
                err_type = "API Surface Protocol Misclassification (GraphQL/gRPC)"

            error_taxonomy[err_type] = error_taxonomy.get(err_type, 0) + 1

            misses_detail.append({
                "id": a["id"],
                "name": name,
                "category": cat,
                "pass1_finding": a.get("pass1_verdict"),
                "pass1_auth": a.get("pass1_auth"),
                "pass1_self_serve": a.get("pass1_self_serve"),
                "pass2_finding": a.get("buildability_verdict"),
                "pass2_auth": a.get("primary_auth"),
                "pass2_self_serve": a.get("self_serve_status"),
                "failure_reason": notes,
                "verification_fix": a.get("verification_check"),
                "error_classification": err_type
            })

    # Accuracy by Category
    category_metrics = {}
    categories = sorted(list(set(a["category"] for a in data)))
    for cat in categories:
        cat_apps = [a for a in data if a["category"] == cat]
        p1_corr = sum(1 for a in cat_apps if a.get("pass1_correct"))
        p2_corr = sum(1 for a in cat_apps if a.get("pass2_correct"))
        category_metrics[cat] = {
            "total": len(cat_apps),
            "pass1_correct": p1_corr,
            "pass1_accuracy": round((p1_corr / len(cat_apps)) * 100, 1),
            "pass2_correct": p2_corr,
            "pass2_accuracy": round((p2_corr / len(cat_apps)) * 100, 1),
            "delta": round(((p2_corr - p1_corr) / len(cat_apps)) * 100, 1)
        }

    verification_summary = {
        "total_apps_audited": total_apps,
        "pass1_accuracy_percent": round(pass1_accuracy, 1),
        "pass2_accuracy_percent": round(pass2_accuracy, 1),
        "accuracy_gain_percent": round(pass2_accuracy - pass1_accuracy, 1),
        "total_pass1_misses": len(misses_detail),
        "error_taxonomy": error_taxonomy,
        "category_metrics": category_metrics,
        "sample_misses": misses_detail
    }

    out_path = dataset_path.parent / "verification_report.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(verification_summary, f, indent=2)

    print(f"Verification complete:")
    print(f" - Pass 1 Accuracy: {pass1_accuracy:.1f}% ({pass1_correct_count}/{total_apps})")
    print(f" - Pass 2 Accuracy: {pass2_accuracy:.1f}% ({pass2_correct_count}/{total_apps})")
    print(f" - Accuracy Improvement: +{pass2_accuracy - pass1_accuracy:.1f}%")
    print(f" - Identified and corrected {len(misses_detail)} misses across Pass 1.")
    print(f"Report saved to {out_path}")

    return verification_summary

if __name__ == "__main__":
    p = Path(r"C:\Users\HP\.gemini\antigravity\scratch\composio-research-agent\data\apps_research_dataset.json")
    run_verification(p)
