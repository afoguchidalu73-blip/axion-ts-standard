cat << 'EOF' > axion/kernel.py
from typing import List, Dict, Any, Set, Tuple

Edge = Tuple[str, str]


def analyze_drift(
    current_trace: List[Dict[str, Any]],
    baseline_trace: List[Dict[str, Any]],
    target_id: str = None
) -> Dict[str, Any]:
    """
    AXION v1.1 - Deterministic Edge Firewall
    """

    def normalize_id(value: Any) -> str:
        if value is None:
            return ""
        return str(value).strip()

    def extract_edges(trace: List[Dict[str, Any]]) -> Set[Edge]:
        edges: Set[Edge] = set()

        for event in trace:
            if not isinstance(event, dict):
                continue

            child = normalize_id(event.get("id"))
            if not child:
                continue

            parents = event.get("parents", [])
            if not isinstance(parents, list):
                parents = [parents]

            for p in parents:
                parent = normalize_id(p)
                if parent:
                    edges.add((parent, child))

        return edges

    base_edges = extract_edges(baseline_trace)
    exec_edges = extract_edges(current_trace)

    missing = base_edges - exec_edges
    extra = exec_edges - base_edges

    if not missing and not extra:
        return {
            "status": "PASSED",
            "cause": None,
            "verified_by": "AXION v1.1"
        }

    violation = list(extra)[0] if extra else list(missing)[0]

    return {
        "status": "BLOCKED",
        "cause": f"Edge Violation: {violation[0]} -> {violation[1]}",
        "details": {
            "missing": sorted(list(missing)),
            "extra": sorted(list(extra))
        },
        "verified_by": "AXION v1.1"
    }
EOF
