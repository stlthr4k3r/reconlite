#!/usr/bin/env python3
# reconlite.py - Simple Python Recon Tool

import argparse
import re
import subprocess

def main():
    parser = argparse.ArgumentParser(
        description="ReconLite - Simple Recon Tool"
    )

    parser.add_argument(
        "target",
        help="Domain or IP address to scan"
    )

    parser.add_argument(
        "--whois",
        action="store_true",
        help="Run a WHOIS lookup on the target"
    )

    arguments = parser.parse_args()
    target = arguments.target

    # Simple validation
    ip_pattern = r"^\d{1,3}(\.\d{1,3}){3}$"
    domain_pattern = r"^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"

    if not (re.match(ip_pattern, target) or re.match(domain_pattern, target)):
        print(f"[-] Invalid domain or IP: {target}")
        exit(1)

    print(f"[+] Target set to: {target}")

    # WHOIS lookup (optional)
    if arguments.whois:
        try:
            print(f"\n[+] Running WHOIS for {target}...\n")
            result = subprocess.run(
                ["whois", target],
                capture_output=True,
                text=True
            )
            print(result.stdout)
        except FileNotFoundError:
            print("[-] WHOIS command not found. Please install 'whois'.")

if __name__ == "__main__":
    main()
