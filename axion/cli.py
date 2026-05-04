import json
import sys
import argparse
from pathlib import Path
from axion.kernel import find_root_cause

def main():
    parser = argparse.ArgumentParser(
        prog="axion",
        description="🛡️ AXION - Deterministic Causal Gate for AI Agent Traces",
        epilog="Expected format: A JSON array of objects with 'id', 'type', 'content', and 'parents'."
    )
    
    parser.add_argument("current", help="Path to the current execution trace (JSON)")
    parser.add_argument("baseline", help="Path to the gold standard trace (JSON)")
    parser.add_argument("--target", default="95", help="The event ID to trace back from (default: 95)")
    parser.add_argument("--json", action="store_true", help="Output results in machine-readable JSON")

    # 1. Handle "No Arguments" gracefully
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    # 2. Defensive File Loading
    data = {}
    for label, path_str in [("current", args.current), ("baseline", args.baseline)]:
        path = Path(path_str)
        
        if not path.exists():
            print(f"❌ [AXION ERROR] File Not Found: The {label} trace '{path_str}' does not exist.")
            sys.exit(2)
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
                if not isinstance(raw_data, list):
                    raise ValueError("Trace must be a JSON list/array.")
                data[label] = {e["id"]: e for e in raw_data if "id" in e}
        except json.JSONDecodeError:
            print(f"❌ [AXION ERROR] Invalid JSON: '{path_str}' is not a valid JSON file.")
            sys.exit(2)
        except Exception as e:
            print(f"❌ [AXION ERROR] {label.capitalize()} Trace Error: {str(e)}")
            sys.exit(2)

    # 3. Defensive Target Check
    if args.target not in data["current"]:
        print(f"⚠️ [AXION WARNING] Target ID '{args.target}' not found in current trace.")
        print(f"Available IDs: {list(data['current'].keys())[:10]}...")
        sys.exit(1)

    # 4. Execute Kernel
    try:
        root = find_root_cause(data["current"], data["baseline"], args.target)
    except Exception as e:
        print(f"💥 [AXION KERNEL CRASH] An unexpected error occurred: {e}")
        sys.exit(3)

    # 5. Structured Output
    if args.json:
        print(json.dumps({
            "status": "blocked" if root else "passed",
            "root_cause": root,
            "target": args.target
        }))
    else:
        print("\n🛡️ AXION Causal Analysis")
        print("-" * 30)
        if root:
            event = data["current"][root]
            print(f"❌ STATUS: BLOCKED")
            print(f"Root Cause Found: Event [{root}]")
            print(f"Drift Content: {event.get('content', 'N/A')}")
        else:
            print("✅ STATUS: PASSED")
            print("No structural drift detected relative to baseline.")

    sys.exit(1 if root else 0)

if __name__ == "__main__":
    main()
      
