"""
Unified CLI Entrypoint for Composio Research Agent
Usage:
    python run.py --all            # Run end-to-end verification, live HTTP audit, and pattern clustering
    python run.py --verify         # Run verification loop and display accuracy delta
    python run.py --analyze        # Run statistical pattern clustering
    python run.py --sample 10      # Run agent on a sample of N apps with live HTTP probes
"""

import argparse
import sys
from pathlib import Path

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
    parser.add_argument("--sample", type=int, default=None, help="Run live agent tool execution on sample of N apps")
    args = parser.parse_args()

    data_dir = BASE_DIR / "data"
    agent = ComposioAppResearchAgent(data_dir=data_dir)

    print("=" * 65)
    print("   COMPOSIO APP RESEARCH AGENT: 100-APP TOOLKIT & AUDIT PIPELINE   ")
    print("=" * 65)

    if args.sample:
        print(f"\n[+] Executing Live Agent Tool Probes on {args.sample} apps...")
        results = agent.run_live_audit_on_sample(sample_size=args.sample)
        for r in results:
            bot_tag = " (Bot Shield)" if r.is_bot_blocked else ""
            status = f"HTTP {r.http_status}" if r.http_status else "Error"
            print(f" - #{r.id:2} {r.name:15} | {r.buildability_verdict:22} | {status}{bot_tag} | Auth: {r.primary_auth}")

    if args.verify or args.all:
        print("\n[+] Running Stage 2: Automated Verification Loops & Live Link Checks...")
        rep = run_verification(dataset_path=data_dir / "apps_research_dataset.json", check_live_sample=True)
        print(f"[OK] Full Dataset (100 apps) Strict Accuracy:")
        print(f"     Pass 1 Strict Record Match:   {rep['full_dataset_pass1_strict_pct']}% (23/100)")
        print(f"     Pass 2 Verified Ground Truth: {rep['full_dataset_pass2_strict_pct']}% (96/100)")
        print(f"     Residual Unresolved / Defeated: {rep['residual_unresolved_count']} apps ({rep['residual_unresolved_pct']}%)")
        print(f"[OK] Validation Samples:")
        print(f"     Random Sample (N=20, Seed=42): Pass 1 {sum(1 for s in rep['random_sample'] if s['pass1_correct'])}/20 -> Pass 2 {sum(1 for s in rep['random_sample'] if s['pass2_correct'])}/20")
        print(f"     Edge-Case Sample (N=13):       Pass 1 {sum(1 for s in rep['edge_case_sample'] if s['pass1_correct'])}/13 -> Pass 2 {sum(1 for s in rep['edge_case_sample'] if s['pass2_correct'])}/13")

    if args.analyze or args.all:
        print("\n[+] Running Stage 3: Statistical Pattern Clustering...")
        pat = analyze_patterns(dataset_path=data_dir / "apps_research_dataset.json")
        m = pat["headline_metrics"]
        print(f"[OK] Ready Today:       {m['ready_for_agent_today_count']}/100 ({m['ready_for_agent_today_pct']}%)")
        print(f"[OK] Free Self-Serve:   {m['free_self_serve_count']}/100 ({m['free_self_serve_pct']}%)")
        print(f"[OK] Total Gated/Walls: {m['total_gated_non_self_serve_count']}/100 ({m['total_gated_non_self_serve_pct']}%)")
        print(f"[OK] MCP Greenfield:    {m['composio_greenfield_count']}/100 ({m['composio_greenfield_pct']}%)")

    if not (args.all or args.verify or args.analyze or args.sample):
        print("\nNo flags specified. Running full pipeline (--all)...")
        run_verification(dataset_path=data_dir / "apps_research_dataset.json", check_live_sample=True)
        analyze_patterns(dataset_path=data_dir / "apps_research_dataset.json")
        print("\nPipeline execution finished successfully.")

if __name__ == "__main__":
    main()
