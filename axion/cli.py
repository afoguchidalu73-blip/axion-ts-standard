cat << 'EOF' > axion/cli.py
import argparse
import json
import sys
from axion.kernel import analyze_drift


def main():
    parser = argparse.ArgumentParser(description="AXION Causal Firewall")
    parser.add_argument("current")
    parser.add_argument("baseline")
    parser.add_argument("--target", default=None)

    args = parser.parse_args()

    try:
        with open(args.current) as f:
            curr = json.load(f)
        with open(args.baseline) as f:
            base = json.load(f)
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        sys.exit(1)

    result = analyze_drift(curr, base, args.target)

    print("\n--- AXION FORENSIC REPORT ---")
    print(f"STATUS: {result['status']}")
    if result.get("cause"):
        print(f"CAUSE: {result['cause']}")
    print("-----------------------------\n")

    if result["status"] == "BLOCKED":
        sys.exit(1)


if __name__ == "__main__":
    main()
EOF
