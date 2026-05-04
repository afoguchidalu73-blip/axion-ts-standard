import json
import sys
import argparse

# -----------------------------
# CORE CAUSAL KERNEL
# -----------------------------
def find_root_cause(curr, gold, target_id):
    visited = set()
    stack = [target_id]

    while stack:
        node_id = stack.pop()
        if node_id in visited:
            continue
        visited.add(node_id)

        curr_e = curr.get(node_id)
        gold_e = gold.get(node_id)

        if not curr_e or not gold_e:
            continue

        # Structural drift check: logic has deviated from gold standard
        if curr_e["content"] != gold_e["content"]:
            parents = curr_e.get("parents", [])
            if not parents:
                return node_id
            # Walk upward to find the absolute earliest deviation
            stack.extend(parents)
            return node_id

    return None

# -----------------------------
# CLI INTERFACE
# -----------------------------
def main():
    parser = argparse.ArgumentParser(
        description="AXION - Causal Execution Diff Kernel"
    )

    parser.add_argument("current", help="Path to the current execution trace")
    parser.add_argument("baseline", help="Path to the gold standard trace")
    parser.add_argument("--target", default="95", help="The event ID to trace back from")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()

    try:
        with open(args.current) as f:
            curr = {e["id"]: e for e in json.load(f)}
        with open(args.baseline) as f:
            gold = {e["id"]: e for e in json.load(f)}
    except Exception as e:
        print(f"[AXION ERROR] Failed to load traces: {e}")
        sys.exit(2) # System Error code

    root = find_root_cause(curr, gold, args.target)

    # OUTPUT MODE: JSON (for CI/CD pipelines)
    if args.json:
        print(json.dumps({
            "status": "blocked" if root else "passed",
            "target": args.target,
            "root_cause": root
        }, indent=2))
        sys.exit(1 if root else 0)

    # OUTPUT MODE: HUMAN (for Developers)
    print("\n🛡️ AXION Causal Gate")
    print("-" * 30)

    if root:
        event = curr[root]
        print("❌ STATUS: BLOCKED")
        print(f"ROOT CAUSE: Event [{root}]")
        print(f"TYPE: {event.get('type', 'Unknown')}")
        print(f"DRIFT: {event.get('content', 'No content summary')}")
        print("\nACTION: Fix causal drift at source before deployment.")
        sys.exit(1) # Failure code (Blocks the build)
    else:
        print("✅ STATUS: PASSED")
        print("No structural drift detected. Deployment safe.")
        sys.exit(0) # Success code

if __name__ == "__main__":
    main()
  
