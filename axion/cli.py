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
            if parents: stack.extend(parents)
    return root

def main():
    parser = argparse.ArgumentParser(description="AXION Causal Gate")
    parser.add_argument("current", help="Path to current trace")
    parser.add_argument("gold", help="Path to gold standard")
    parser.add_argument("--target", default="95", help="Target Event ID")
    args = parser.parse_args()

    try:
        with open(args.current) as f: curr = {e['id']: e for e in json.load(f)}
        with open(args.gold) as f: gold = {e['id']: e for e in json.load(f)}
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    root_id = find_root_cause(curr, gold, args.target)
    if root_id:
        print(f"❌ BLOCKED: Drift at [{root_id}]")
        sys.exit(1)
    else:
        print("✅ PASSED")
  
