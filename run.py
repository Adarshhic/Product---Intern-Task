"""
Unified CLI Entrypoint for Composio Research Agent
Usage:
    python run.py --all            # Run end-to-end extraction, verification, analysis, and build HTML
    python run.py --verify         # Run verification loop and display accuracy delta
    python run.py --analyze        # Run pattern clustering and output insights
    python run.py --sample 10      # Run agent on a sample of 10 apps
"""

import argparse
import sys
from pathlib import Path

# Ensure src is on path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from src.agent import ComposioAppResearchAgent
from src.verifier import run_verification
from src.analyzer import analyze_patterns

def main():
    parser = argparse.ArgumentParser(description="Composio App Research Agent Runner")
    parser.add_argument("--all", action="store_true", help="Execute complete pipeline end-to-end")
    parser.add_argument("--verify", action="store_true", help="Run verification loops and accuracy audit")
    parser.add_argument("--analyze", action="store_true", help="Run statistical pattern clustering")
    parser.add_argument("--sample", type=int, default=None, help="Run on a sample of N apps")
    args = parser.parse_args()

    data_dir = BASE_DIR / "data"
    agent = ComposioAppResearchAgent(data_dir=data_dir)

    print("=" * 60)
    print("   COMPOSIO APP RESEARCH AGENT: 100-APP TOOLKIT AUDIT   ")
    print("=" * 60)

    if args.verify or args.all:
        print("\n[+] Running Stage 2: Automated Verification Loops...")
        rep = run_verification(data_dir / "apps_research_dataset.json")
        print(f"[OK] Pass 1 Accuracy: {rep['pass1_accuracy_percent']}% -> Pass 2 Accuracy: {rep['pass2_accuracy_percent']}%")
        print(f"[OK] Accuracy Gain: +{rep['accuracy_gain_percent']}% across {rep['total_apps_audited']} audited apps.")

    if args.analyze or args.all:
        print("\n[+] Running Stage 3: Pattern Clustering & Macro Analysis...")
        pat = analyze_patterns(data_dir / "apps_research_dataset.json")
        print(f"[OK] Ready Today: {pat['headline_metrics']['ready_for_agent_today_pct']}%")
        print(f"[OK] Free Self-Serve: {pat['headline_metrics']['free_self_serve_pct']}%")
        print(f"[OK] Composio MCP Opportunity: {pat['headline_metrics']['composio_greenfield_pct']}%")

    if args.sample:
        print(f"\n[+] Running Agent Extraction on Sample of {args.sample} apps...")
        results = agent.run_pass1(sample_size=args.sample)
        for r in results:
            print(f" - #{r['id']} {r['name']}: {r['buildability_verdict']} | Auth: {r['primary_auth']} | Gating: {r['self_serve_status']}")

    if not (args.all or args.verify or args.analyze or args.sample):
        # Default behavior: run all
        print("\nNo flags specified. Running full pipeline (--all)...")
        run_verification(data_dir / "apps_research_dataset.json")
        analyze_patterns(data_dir / "apps_research_dataset.json")
        print("\nPipeline execution finished successfully.")
        print("Generated files:")
        print(f"  - Dataset (JSON): {data_dir / 'apps_research_dataset.json'}")
        print(f"  - Dataset (CSV):  {data_dir / 'apps_research_dataset.csv'}")
        print(f"  - Verification:  {data_dir / 'verification_report.json'}")
        print(f"  - Patterns:      {data_dir / 'pattern_analysis.json'}")

if __name__ == "__main__":
    main()
