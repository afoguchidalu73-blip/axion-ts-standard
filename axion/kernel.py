def analyze_drift(current_trace, baseline_trace, target_id=None):
    """
    AXION v1.1 Kernel
    Deterministic Edge Set Integrity Checker

    Rule:
    Execution is valid ONLY if edge sets match exactly.
    """

    def extract_edges(trace):
        edges = set()

        if not isinstance(trace, list):
            return edges

        for event in trace:
            if not isinstance(event, dict):
                continue

            child = str(event.get("id"))
            parents = event.get("parents", [])

            # Normalize single-parent case
            if isinstance(parents, str):
                parents = [parents]

            if not isinstance(parents, list):
                parents = []

            for p in parents:
                if p is None:
                    continue

                edges.add((str(p), child))

        return edges

    # -------------------------
    # Build canonical edge sets
    # -------------------------
    base_edges = extract_edges(baseline_trace)
    exec_edges = extract_edges(current_trace)

    # -------------------------
    # Compare sets (STRICT MODE)
    # -------------------------
    missing = base_edges - exec_edges
    extra = exec_edges - base_edges

    # -------------------------
    # PASS CONDITION
    # -------------------------
    if len(missing) == 0 and len(extra) == 0:
        return {
            "status": "PASSED",
            "cause": None,
            "details": {
                "missing": [],
                "extra": []
            }
        }

    # -------------------------
    # FAILURE MODE
    # -------------------------
    violation = None

    if extra:
        violation = list(extra)[0]
        reason = "EXTRA_EDGE (possible injection/hijack)"
    else:
        violation = list(missing)[0]
        reason = "MISSING_EDGE (broken causal link)"

    return {
        "status": "BLOCKED",
        "cause": f"{reason}: {violation[0]} -> {violation[1]}",
        "details": {
            "missing": list(missing),
            "extra": list(extra)
        }
      }
