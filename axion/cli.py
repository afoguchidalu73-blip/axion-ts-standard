print("AXION CLI STARTED")
import argparse
import json
import sys
from axion.kernel import analyze_drift


# ----------------------------
# Safe file loader
# ----------------------------
def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ ERROR: File not found → {path}")
        sys.exit(2)
    except json.JSONDecodeError:
        print(f"❌ ERROR: Invalid JSON → {path}")
        sys.exit(2)
    except Exception as e:
        print(f"❌ ERROR: Unexpected failure loading {path}: {e}")
        sys.exit(2)


# ----------------------------
# Output formatter
# ----------------------------
def print_result(result, json_mode=False):
    if json_mode:
        print(json.dumps(result, indent=2))
        return

    if result["status"] == "BLOCKED":
        print("\n❌ AXION: BLOCKED")
        print(f"CAUSE: {result.get('cause')}")
        if result.get("details"):
            print(f"DETAILS: {result['details']}")
    else:
        print("\n✅ AXION: PASSED")


# ----------------------------
# CLI entrypoint
# ----------------------------
def main():
    parser = argparse.ArgumentParser(description="AXION Causal Integrity Gate")

    parser.add_argument("current", help="Execution trace JSON")
    parser.add_argument("baseline", help="Baseline trace JSON")
    parser.add_argument("--json", action="store_true", help="Machine output mode")

    args = parser.parse_args()

    # 1. Load inputs safely
    current = load_json(args.current)
    baseline = load_json(args.baseline)

    # 2. Run kernel
    result = analyze_drift(current, baseline)

    # 3. Print output
    print_result(result, args.json)

    # 4. CRITICAL: exit codes (THIS is your CI gate)
    if result["status"] == "BLOCKED":
        sys.exit(1)   # 🔴 FAIL PIPELINE
    else:
        sys.exit(0)   # 🟢 PASS PIPELINE


if __name__ == "__main__":
    main()
