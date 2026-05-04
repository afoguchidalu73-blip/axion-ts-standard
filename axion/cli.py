cat << 'EOF' > axion/cli.py
import json
import argparse
import sys

from axion.kernel import analyze_drift


def main():
    parser = argparse.ArgumentParser(
        description="AXION v1.1 - Causal Firewall"
    )
    parser.add_argument("current", help="Path to current trace JSON")
    parser.add_argument("baseline", help="Path to baseline trace JSON")
    parser.add_argument("--target", default=None, help="Target node ID")

    args = parser.parse_args()

    try:
        with open(args.current) as f:
            current = json.load(f)

        with open(args.baseline) as f:
            baseline = json.load(f)

    except Exception as e:
        print(f"❌ FILE ERROR: {e}")
        sys.exit(1)

    result = analyze_drift(current, baseline, args.target)

    print("\n🛡️ AXION CAUSAL FIREWALL v1.1")
    print("-" * 40)
    print(f"STATUS: {result['status']}")

    if result["status"] == "BLOCKED":
        print(f"CAUSE: {result.get('cause')}")
        print(f"EXTRA: {result.get('extra')}")
        print(f"MISSING: {result.get('missing')}")
        sys.exit(1)

    print("✅ No structural drift detected")


if __name__ == "__main__":
    main()
EOF
