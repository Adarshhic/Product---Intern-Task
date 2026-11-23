"""
Unit Tests for Composio Research Agent Pipeline
"""

import json
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

    def test_dataset_size_and_schema(self):
        with open(self.dataset_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(len(data), 100, "Dataset must contain exactly 100 apps")
        
        required_fields = [
            "id", "name", "category", "description", "auth_methods", "primary_auth",
            "self_serve_status", "api_surface", "mcp_status", "buildability_verdict",
            "main_blocker", "evidence_url", "pass1_correct", "pass2_correct"
        ]
        for app in data:
            for field in required_fields:
                self.assertIn(field, app, f"Missing field {field} in app #{app.get('id')}")

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
        self.assertGreater(report["full_dataset_pass2_accuracy_pct"], report["full_dataset_pass1_accuracy_pct"])
        self.assertGreater(report["sample_pass2_accuracy_pct"], report["sample_pass1_accuracy_pct"])

    def test_pattern_analysis(self):
        analysis = analyze_patterns(self.dataset_file)
        self.assertEqual(analysis["metadata"]["total_apps"], 100)
        self.assertIn("ready_for_agent_today_pct", analysis["headline_metrics"])
        self.assertEqual(analysis["headline_metrics"]["ready_for_agent_today_count"], 80)
        self.assertEqual(analysis["headline_metrics"]["total_gated_non_self_serve_count"], 16)

if __name__ == "__main__":
    unittest.main()
