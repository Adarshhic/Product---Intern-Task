"""
Composio Research Agent: Multi-Stage Automated App Intelligence Pipeline
Simulates an agentic pipeline with tool calling, multi-pass reasoning,
automated verification loops, and human-in-the-loop review.
"""

import json
import logging
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ComposioResearchAgent")

@dataclass
class AppInput:
    id: int
    name: str
    category: str
    website_hint: str

@dataclass
class Pass1Output:
    id: int
    name: str
    category: str
    description: str
    primary_auth: str
    self_serve_status: str
    api_surface: str
    buildability_verdict: str
    evidence_url: str
    notes: str

@dataclass
class VerifiedAppResult:
    id: int
    name: str
    category: str
    description: str
    auth_methods: List[str]
    primary_auth: str
    self_serve_status: str
    self_serve_details: str
    api_surface: str
    mcp_status: str
    buildability_verdict: str
    main_blocker: str
    evidence_url: str
    verification_check: str
    confidence_score: float

class ComposioAppResearchAgent:
    """
    Agent architecture for evaluating app buildability for AI toolkits.
    Implements a 3-stage pipeline:
      Stage 1: Automated Web/Docs Extraction (Pass 1)
      Stage 2: Verification Loop & Discrepancy Detection (Pass 2)
      Stage 3: Human-in-the-Loop Anomaly Resolution & Final Grounding
    """

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.input_file = data_dir / "apps_input.json"
        self.verified_file = data_dir / "apps_research_dataset.json"

    def load_inputs(self) -> List[AppInput]:
        with open(self.input_file, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return [AppInput(**item) for item in raw]

    def tool_fetch_docs_evidence(self, app_name: str, hint: str) -> str:
        """Simulated agent tool: looks up canonical developer docs URL."""
        if "http" in hint:
            return f"https://{hint}" if not hint.startswith("http") else hint
        return f"https://developer.{hint.split()[0]}"

    def tool_check_mcp_registry(self, app_name: str) -> str:
        """Simulated agent tool: queries GitHub and Model Context Protocol registries."""
        known_mcp = {
            "Slack", "GitHub", "Cloudflare", "Neo4j", "Sentry", "Apify", 
            "Firecrawl", "Devin", "Salesforce", "HubSpot", "Twenty", "Zoho CRM",
            "Close", "Zendesk", "Intercom", "Twilio", "Lark (Larksuite)", "Discord",
            "Telegram", "WhatsApp Business", "Google Ads", "GoHighLevel", "Mailchimp",
            "Klaviyo", "SendGrid", "Shopify", "WooCommerce", "DataForSEO", "Ahrefs",
            "Bright Data", "Sherlock", "Clay", "Vercel", "Netlify", "Supabase",
            "Snowflake", "MongoDB Atlas", "Datadog", "Notion", "Airtable", "Linear",
            "Jira", "Asana", "Monday.com", "ClickUp", "Coda", "Stripe", "Plaid",
            "Binance", "QuickBooks", "Xero", "NotebookLM", "Otter AI", "Reducto",
            "Mermaid CLI", "YouTube Transcript"
        }
        if app_name in {"GitHub", "Slack", "Cloudflare", "Neo4j", "Sentry", "Apify", "Firecrawl", "Devin"}:
            return "Official MCP Available"
        elif app_name in known_mcp:
            return "Community MCP Available"
        return "No MCP (Composio Opportunity)"

    def run_pass1(self, sample_size: Optional[int] = None) -> List[Dict[str, Any]]:
        """Pass 1: Automated extraction pass across target apps."""
        logger.info("Executing Pass 1: Automated extraction pass...")
        with open(self.data_dir / "pass1_results.json", "r", encoding="utf-8") as f:
            pass1 = json.load(f)
        if sample_size:
            pass1 = pass1[:sample_size]
        logger.info(f"Pass 1 complete. Extracted {len(pass1)} app records.")
        return pass1

    def run_verification_loop(self) -> Dict[str, Any]:
        """Pass 2: Runs automated verification loop and flags discrepancies."""
        from src.verifier import run_verification
        logger.info("Executing Pass 2: Running Verification Loops...")
        return run_verification(self.verified_file)

    def run_pattern_analysis(self) -> Dict[str, Any]:
        """Stage 4: Extracts macro clustering patterns and actionable insights."""
        from src.analyzer import analyze_patterns
        logger.info("Executing Pattern Analysis: Clustering trends across 100 apps...")
        return analyze_patterns(self.verified_file)

    def get_full_dataset(self) -> List[Dict[str, Any]]:
        with open(self.verified_file, "r", encoding="utf-8") as f:
            return json.load(f)
