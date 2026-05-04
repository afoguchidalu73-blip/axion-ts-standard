cat << 'EOF' > axion/kernel.py
def analyze_drift(current_trace, baseline_trace, target_id=None):
    """
    AXION v1.1 - Deterministic Edge Firewall
    """

    def extract_edges(trace):
        edges = set()
        for event in trace:
            if not isinstance(event, dict):
                continue

            child = str(event.get("id", "")).strip()
            if not child:
                continue

            parents = event.get("parents", [])
            if not isinstance(parents, list):
                parents = [parents]

            for p in parents:
                p = str(p).strip()
                if p:
                    edges.add((p, child))

        return edges

    base_edges = extract_edges(baseline_trace)
    exec_edges = extract_edges(current_trace)

    missing = base_edges - exec_edges
    extra = exec_edges - base_edges

    if not missing and not extra:
        return {"status": "PASSED"}

    violation = next(iter(extra)) if extra else next(iter(missing))

    return {
        "status": "BLOCKED",
        "cause": f"Edge Violation: {violation[0]} -> {violation[1]}",
        "missing": list(missing),
        "extra": list(extra)
    }
EOF
