def find_root_cause(curr, gold, target_id):
    """Pure logic: no prints, no sys.exit, just causal backtracking."""
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

        if curr_e.get("content") != gold_e.get("content"):
            parents = curr_e.get("parents", [])
            if not parents:
                return node_id
            stack.extend(parents)
            return node_id
    return None
  
