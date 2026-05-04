import sys
import json
from axion.kernel import analyze_drift


def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ FILE NOT FOUND: {path}")
        sys.exit(2)
    except json.JSONDecodeError:
        print(f"❌ INVALID JSON: {path}")
        sys.exit(2)


def main():
    # -------------------------
    # BASIC ARG CHECK (no argparse bugs possible)
    # -------------------------
    if len(sys.argv) != 3:
        print("\n🛡️ AXION CLI")
        print("Usage:")
        print("  axion <current.json> <baseline.json>\n")
        sys.exit(2)

    current_path = sys.argv[1]
    baseline_path = sys.argv[2]

    current = load_json(current_path)
    baseline = load_json(baseline_path)

    result = analyze_drift(current, baseline)

    print("\n🛡️ AXION CAUSAL GATE")
    print("-" * 40)

    if result["status"] == "PASSED":
        print("✅ STATUS: PASSED")
        sys.exit(0)

    print("❌ STATUS: BLOCKED")
    print(f"ROOT CAUSE: {result['cause']}")

    # optional debug mode
    if result.get("details"):
        print("\nDETAILS:")
        print(json.dumps(result["details"], indent=2))

    sys.exit(1)


if __name__ == "__main__":
    main()
