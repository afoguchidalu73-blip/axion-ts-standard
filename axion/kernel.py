cat <<EOF > axion/kernel.py
def analyze_drift(current_trace, baseline_trace, target_id):
    """Strict structural verification of causal parents."""
    # Create lookups
    curr_map = {item['id']: item for item in current_trace}
    base_map = {item['id']: item for item in baseline_trace}
    
    if target_id not in curr_map or target_id not in base_map:
        return {"status": "ERROR", "cause": "Target ID missing"}

    # Check direct parents
    curr_parents = set(curr_map[target_id].get('parents', []))
    base_parents = set(base_map[target_id].get('parents', []))

    if curr_parents != base_parents:
        # Identify the exact ID that shouldn't be there
        drift = list(curr_parents - base_parents)
        return {
            "status": "BLOCKED", 
            "cause": drift[0] if drift else "Unknown Structural Drift"
        }
    
    return {"status": "PASSED", "cause": None}
EOF
      
