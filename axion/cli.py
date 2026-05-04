import sys, json, argparse
from axion.kernel import analyze_drift

def print_report(res, is_json):
    """Handles the Pro UI and JSON output modes."""
    if is_json:
        print(json.dumps(res, indent=2))
        return

    status_icon = "❌" if res['status'] == "BLOCKED" else "✅"
    print(f"\n🛡️  AXION PRO — Causal Gate")
    print(f"{status_icon} STATUS: {res['status']}")
    
    if res['status'] == "BLOCKED":
        print(f"\nViolation Details:")
        print(f"  Issue: {res.get('cause', 'Causal integrity failure')}")
        
        if res.get('extra'):
            print("\n  Unexpected Edges (Injected):")
            for e in res['extra']: 
                print(f"    - {e[0]} → {e[1]}")
            
        if res.get('missing'):
            print("\n  Missing Edges (Broken):")
            for m in res['missing']: 
                print(f"    - {m[0]} → {m[1]}")
            
        print("\nACTION: Deployment halted. Restore causal integrity.")
    else:
        print("\nACTION: Causal integrity verified. Proceed with deployment.")
    print("-" * 30 + "\n")

def main():
    p = argparse.ArgumentParser(prog="axion", description="Pro Causal Audit Tool")
    sub = p.add_subparsers(dest="command", help="Available commands")
    
    # 'gate' command: The primary entry point for CI/CD pipelines
    gate = sub.add_parser("gate", help="Verify causal integrity and return exit codes")
    gate.add_argument("curr", help="Path to the current execution trace")
    gate.add_argument("base", help="Path to the gold-standard baseline")
    gate.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    
    args = p.parse_args()
    
    if not args.command:
        p.print_help()
        return

    try:
        # Load data with standard JSON parser
        with open(args.curr) as f: 
            current_data = json.load(f)
        with open(args.base) as f: 
            baseline_data = json.load(f)
        
        # Execute the Truth Engine
        result = analyze_drift(current_data, baseline_data)
        
        # Display the professional report
        print_report(result, args.json)
        
        # Critical for Pro Tooling: Return exit code 1 if blocked to stop CI/CD
        sys.exit(1 if result['status'] == "BLOCKED" else 0)
        
    except FileNotFoundError as e:
        print(f"❌ Error: Could not find file - {e.filename}")
        sys.exit(2)
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        sys.exit(2)

if __name__ == "__main__":
    main()
  
