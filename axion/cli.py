import argparse
import json
import sys

from axion.kernel import analyze_drift


def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ ERROR: File not found -> {path}")
        sys.exit(2)
    except json.JSONDecodeError:
        print(f"❌ ERROR: Invalid JSON -> {path}")
        sys.exit(2)


def main():
    parser = argparse.ArgumentParser(
        prog="axion",
        description="AXION: Deterministic Causal Gate for AI Agent Traces"
    )

    # ✅ SIMPLE POSITIONAL INTERFACE (NO SUBCOMMANDS)
    parser.add_argument("current", help="Path to execution trace (drifted)")
    parser.add_argument("baseline", help="Path to baseline trace (gold standard)")
    parser.add_argument("--target", default=None, help="Optional target node id")
    parser.add_argument("--json", action="store_true", help="Output JSON format")

    args = parser.parse_args()

    current_trace = load_json(args.current)
    baseline_trace = load_json(args.baseline)

    result = analyze_drift(
        current_trace=current_trace,
        baseline_trace=baseline_trace,
        target_id=args.target
    )

    # -------------------------
    # OUTPUT MODE: MACHINE
    # -------------------------
    if args.json:
        print(json.dumps(result, indent=2))
        sys.exit(1 if result["status"] == "BLOCKED" else 0)

    # -------------------------
    # OUTPUT MODE: HUMAN
    # -------------------------
    print("\n🛡️ AXION CAUSAL GATE")
    print("-" * 40)

    if result["status"] == "PASSED":
        print("✅ STATUS: PASSED")
        print("No structural drift detected.")
        sys.exit(0)

    # BLOCKED PATH
    print("❌ STATUS: BLOCKED")
    print(f"ROOT CAUSE: {result.get('cause')}")

    if "details" in result:
        if result["details"].get("extra"):
            print("\n⚠️ EXTRA EDGES DETECTED:")
            for e in result["details"]["extra"]:
                print(f"   {e[0]} → {e[1]}")

        if result["details"].get("missing"):
            print("\n⚠️ MISSING EDGES:")
            for e in result["details"]["missing"]:
                print(f"   {e[0]} → {e[1]}")

    sys.exit(1)


if __name__ == "__main__":
    main()
