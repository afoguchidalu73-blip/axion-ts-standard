import json
import sys
import argparse

def find_root_cause(curr, gold, start_id):
    visited = set()
    stack = [start_id]
    root = None
    while stack:
        node_id = stack.pop()
        if node_id in visited: continue
        visited.add(node_id)
        curr_e, gold_e = curr.get(node_id), gold.get(node_id)
        if not curr_e or not gold_e: continue
        
        if curr_e.get('content') != gold_e.get('content'):
            root = node_id
            parents = curr_e.get('parents', [])
            if parents:
                stack.extend(parents)
    return root

def build_chain(curr, start_id):
    chain = []
    node = start_id
    while node:
        chain.append(node)
        parents = curr.get(node, {}).get("parents", [])
        node = parents[0] if parents else None
    return list(reversed(chain))

def main():
    parser = argparse.ArgumentParser(description="AXION Causal Gate")
    parser.add_argument("current", help="Path to current trace JSON")
    parser.add_argument("gold", help="Path to gold standard JSON")
    parser.add_argument("--target", default="95", help="Target Event ID to check")
    parser.add_argument("--fail-on", default="INV", help="Failure condition (INV)")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    args = parser.parse_args()

    try:
        with open(args.current) as f: curr = {e['id']: e for e in json.load(f)}
        with open(args.gold) as f: gold = {e['id']: e for e in json.load(f)}
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    root_id = find_root_cause(curr, gold, args.target)

    if args.json:
        output = {
            "status": "failed" if root_id else "passed",
            "root_cause": root_id,
            "chain": build_chain(curr, args.target),
            "diff": {
                "expected": gold[root_id]['content'] if root_id else None,
                "actual": curr[root_id]['content'] if root_id else None
            } if root_id else None
        }
        print(json.dumps(output, indent=2))
    else:
        print("\n🛡️ AXION PRO: Causal Gate Evaluation")
        print("-" * 50)
        if root_id:
            print(f"❌ STATUS: BLOCKED ({args.fail_on} Violation)")
            print(f"ROOT CAUSE: Event [{root_id}]")
            print(f"EXPECTED:   {gold[root_id]['content']}")
            print(f"ACTUAL:     {curr[root_id]['content']}")
            print("-" * 50)
        else:
            print(f"✅ STATUS: PASSED")

    if root_id and args.fail_on == "INV":
        sys.exit(1)

if __name__ == "__main__":
    main()
  
