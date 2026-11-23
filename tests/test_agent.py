"""
Unit Tests for Composio Research Agent Pipeline & Mathematical Consistency
"""

import json
import re
import unittest
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.agent import ComposioAppResearchAgent
from src.verifier import run_verification
from src.analyzer import analyze_patterns

class TestComposioResearchAgent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data_dir = BASE_DIR / "data"
        cls.dataset_file = cls.data_dir / "apps_research_dataset.json"
        cls.readme_file = BASE_DIR / "README.md"
        cls.html_file = BASE_DIR / "index.html"

    def test_dataset_size_and_schema(self):
        with open(self.dataset_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(len(data), 100, "Dataset must contain exactly 100 apps")
        
        required_fields = [
            "id", "name", "category", "description", "auth_methods", "primary_auth",
            "self_serve_status", "api_surface", "mcp_status", "buildability_verdict",
            "main_blocker", "notes", "evidence_url"
        ]
        for app in data:
            for field in required_fields:
                self.assertIn(field, app, f"Missing field {field} in app #{app.get('id')}")
            # Ensure blocker is clean: Ready Today must have exactly 'None'
            if app["buildability_verdict"] == "Ready Today":
                self.assertEqual(app["main_blocker"], "None", f"Ready app #{app['id']} {app['name']} blocker should be 'None', got '{app['main_blocker']}'")

    def test_ten_categories_represented(self):
        with open(self.dataset_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        categories = set(a["category"] for a in data)
        self.assertEqual(len(categories), 10, "There should be exactly 10 distinct categories")
        for cat in categories:
            cat_count = sum(1 for a in data if a["category"] == cat)
            self.assertEqual(cat_count, 10, f"Category {cat} should have exactly 10 apps")

    def test_verification_metrics(self):
        report = run_verification(self.dataset_file, check_live_sample=False)
        self.assertEqual(report["total_apps_audited"], 100)
        self.assertEqual(report["full_dataset_pass1_strict_pct"], 51.0)
        self.assertEqual(report["full_dataset_pass2_strict_pct"], 98.0)
        self.assertEqual(report["residual_unresolved_count"], 2)
        self.assertEqual(len(report["random_sample"]), 10)
        self.assertEqual(len(report["edge_case_sample"]), 10)
        self.assertEqual(len(report["audit_sample_20"]), 20)
        self.assertEqual(len(report["hard_cases"]), 4)

    def test_pattern_analysis(self):
        analysis = analyze_patterns(self.dataset_file)
        metrics = analysis["headline_metrics"]
        self.assertEqual(analysis["metadata"]["total_apps"], 100)
        self.assertEqual(metrics["ready_for_agent_today_count"], 81)
        self.assertEqual(metrics["feasible_with_caveats_count"], 10)
        self.assertEqual(metrics["gated_partner_required_count"], 8)
        self.assertEqual(metrics["blocked_no_api_count"], 1)
        self.assertEqual(metrics["free_self_serve_count"], 74)
        self.assertEqual(metrics["paid_self_serve_count"], 11)
        self.assertEqual(metrics["total_self_serve_count"], 85)
        self.assertEqual(metrics["total_gated_non_self_serve_count"], 15)
        self.assertEqual(metrics["composio_greenfield_count"], 42)

    def test_no_metric_drift_between_json_readme_and_html(self):
        """Ensures that README.md and index.html strictly agree with the recomputed dataset metrics."""
        analysis = analyze_patterns(self.dataset_file)
        metrics = analysis["headline_metrics"]
        
        ready_pct_str = f"{int(metrics['ready_for_agent_today_pct'])}%"
        free_ss_pct_str = f"{int(metrics['free_self_serve_pct'])}%"
        total_ss_pct_str = f"{int(metrics['total_self_serve_pct'])}%"
        gated_pct_str = f"{int(metrics['total_gated_non_self_serve_pct'])}%"
        greenfield_pct_str = f"{int(metrics['composio_greenfield_pct'])}%"

        with open(self.readme_file, "r", encoding="utf-8") as f:
            readme_text = f.read()
        with open(self.html_file, "r", encoding="utf-8") as f:
            html_text = f.read()

        # Check README agreement
        self.assertIn(ready_pct_str, readme_text, f"README missing {ready_pct_str}")
        self.assertIn(free_ss_pct_str, readme_text, f"README missing {free_ss_pct_str}")
        self.assertIn(total_ss_pct_str, readme_text, f"README missing {total_ss_pct_str}")
        self.assertIn(gated_pct_str, readme_text, f"README missing {gated_pct_str}")
        self.assertIn(greenfield_pct_str, readme_text, f"README missing {greenfield_pct_str}")

        # Check HTML agreement
        self.assertIn(ready_pct_str, html_text, f"index.html missing {ready_pct_str}")
        self.assertIn(free_ss_pct_str, html_text, f"index.html missing {free_ss_pct_str}")
        self.assertIn(total_ss_pct_str, html_text, f"index.html missing {total_ss_pct_str}")
        self.assertIn(gated_pct_str, html_text, f"index.html missing {gated_pct_str}")
        self.assertIn(greenfield_pct_str, html_text, f"index.html missing {greenfield_pct_str}")

    def test_audit_sample_table_consistency(self):
        """Verifies that the 20-app sample table in HTML contains exactly 20 rows matching the verifier."""
        report = run_verification(self.dataset_file, check_live_sample=False)
        with open(self.html_file, "r", encoding="utf-8") as f:
            html_text = f.read()

        for s in report["audit_sample_20"]:
            self.assertIn(s["name"], html_text, f"Audit sample app {s['name']} missing from HTML table")
            self.assertIn(s["sample_type"], html_text, f"Sample type {s['sample_type']} for {s['name']} missing from HTML")

if __name__ == "__main__":
    unittest.main()
