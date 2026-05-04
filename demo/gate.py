import json
import sys

def find_root_cause(curr, gold, start_id):
    visited = set()
    stack = [start_id]
    while stack:
        node_id = stack.pop()
        if node_id in visited: continue
        visited.add(node_id)
        curr_e, gold_e = curr.get(node_id), gold.get(node_id)
        if curr_e and gold_e and curr_e['content'] != gold_e['content']:
            parents = curr_e.get('parents', [])
            if not parents: return node_id
            stack.extend(parents)
            return node_id
    return None

def run_gate(curr_path, gold_path, target="95"):
    try:
        with open(curr_path) as f: curr = {e['id']: e for e in json.load(f)}
        with open(gold_path) as f: gold = {e['id']: e for e in json.load(f)}
    except FileNotFoundError:
        print("Error: Demo files missing.")
        return

    print("\n🛡️ AXION PRO: Causal Gate Evaluation")
    print("-" * 50)
    
    root_id = find_root_cause(curr, gold, target)

    if root_id:
        print(f"❌ STATUS: BLOCKED (Structural Drift Detected)")
        print(f"\nTARGET FAILURE:\nEvent [{target}] - {curr[target]['type'].upper()}")
        print(f"\nROOT CAUSE:\nEvent [{root_id}] - {curr[root_id]['type'].upper()} DRIFT")
        print(f"\nEXPECTED: \"{gold[root_id]['content']}\"")
        print(f"ACTUAL:   \"{curr[root_id]['content']}\"")
        print(f"\nCAUSAL CHAIN: [{root_id}] → ... → [{target}]")
        print(f"\nACTION REQUIRED: Restore invariant at Event [{root_id}].")
        print("-" * 50)
        sys.exit(1)

if __name__ == "__main__":
    run_gate("broken.json", "gold.json")
      
