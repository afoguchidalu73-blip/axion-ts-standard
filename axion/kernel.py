"""
AXION CAUSAL KERNEL v1.1
Lead Engineer: Chief
Status: Deterministic / Production-Ready
"""

from typing import List, Dict, Any, Set, Tuple

# Type definition for a causal link (Parent ID -> Child ID)
Edge = Tuple[str, str]

def analyze_drift(current_trace: List[Dict[str, Any]],
                   baseline_trace: List[Dict[str, Any]],
                   target_id: str = None) -> Dict[str, Any]:
    """
    Deterministic Edge-Set Firewall.
    Enforces that every execution handshake matches the gold standard.
    """

    def normalize_id(value: Any) -> str:
        """Force stable string identity for IDs to prevent type-mismatch errors."""
        if value is None:
            return ""
        return str(value).strip()

    def extract_edges(trace: List[Dict[str, Any]]) -> Set[Edge]:
        """Convert a trace into a set of canonical causal edges (parent -> child)."""
        edges: Set[Edge] = set()
        for event in trace:
            if not isinstance(event, dict):
                continue
            
            child = normalize_id(event.get("id"))
            if not child:
                continue

            parents = event.get("parents", [])
            
            # Defensive normalization for various parent formats
            if parents is None:
                parents = []
            elif isinstance(parents, (str, int)):
                parents = [parents]
            elif not isinstance(parents, list):
                continue
                
            for p in parents:
                parent = normalize_id(p)
                if parent:
                    edges.add((parent, child))
        return edges

    # 1. Generate Canonical Edge Sets from both traces
    base_edges = extract_edges(baseline_trace)
    exec_edges = extract_edges(current_trace)

    # 2. Set-Theoretic Comparison (The Firewall Heart)
    missing_edges = base_edges - exec_edges
    extra_edges = exec_edges - base_edges

    # 3. Decision Logic
    if not missing_edges and not extra_edges:
        return {
            "status": "PASSED",
            "cause": None,
            "verified_by": "Chief",
            "missing": [],
            "extra": []
        }

    # 4. Identify the primary violation for the summary report
    primary = next(iter(extra_edges), None) or next(iter(missing_edges), None)

    return {
        "status": "BLOCKED",
        "cause": f"Edge Violation: {primary[0]} -> {primary[1]}",
        "verified_by": "Chief",
        "missing": sorted(list(missing_edges)),
        "extra": sorted(list(extra_edges))
      }
                     
