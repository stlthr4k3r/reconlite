import subprocess
import re
import argparse

def parse_whois(whois_output):
    """
    Extract Registrar, Creation Date, and Name Servers from WHOIS output.
    Returns a dictionary with structured data.
    """
    # Match "Registrar:" or fallback "Registrar Name:"
    registrar_match = re.search(r"Registrar:\s*(.+)", whois_output, re.IGNORECASE)
    if not registrar_match:
        registrar_match = re.search(r"Registrar Name:\s*(.+)", whois_output, re.IGNORECASE)
    registrar = registrar_match.group(1).strip() if registrar_match else "Not found"

    # Match "Creation Date:" or fallback "Created On:"
    creation_match = re.search(r"Creation Date:\s*(.+)", whois_output, re.IGNORECASE)
    if not creation_match:
        creation_match = re.search(r"Created On:\s*(.+)", whois_output, re.IGNORECASE)
    creation_date = creation_match.group(1).strip() if creation_match else "Not found"

    # Match all "Name Server:" entries
    name_servers = re.findall(r"Name Server:\s*(.+)", whois_output, re.IGNORECASE)
    name_servers = [ns.strip() for ns in name_servers] if name_servers else []

    return {
        "registrar": registrar,
        "creation_date": creation_date,
        "name_servers": name_servers
    }

def print_whois(parsed):
    """Nicely prints a parsed WHOIS dictionary"""
    print("\n[+] WHOIS Summary:")
    print(f"    Registrar: {parsed['registrar']}")
    print(f"    Creation Date: {parsed['creation_date']}")
    print("    Name Servers:")
    if parsed["name_servers"]:
        for ns in parsed["name_servers"]:
            print(f"        - {ns}")
    else:
        print("        Not found")

def main():
    parser = argparse.ArgumentParser(description="ReconLite - Simple Recon Tool")
    parser.add_argument("target", help="Target domain or IP")
    parser.add_argument("--whois", action="store_true", help="Run WHOIS lookup")
    arguments = parser.parse_args()

    target = arguments.target

    if arguments.whois:
        try:
            print(f"\n[+] Running WHOIS for {target}...\n")
            result = subprocess.run(
                ["whois", target],
                capture_output=True,
                text=True
            )
            whois_output = result.stdout

            if not whois_output.strip():
                print("[-] WHOIS returned empty output.")
                return

            # Parse and print WHOIS info
            parsed = parse_whois(whois_output)
            print_whois(parsed)

        except FileNotFoundError:
            print("[-] WHOIS command not found. Please install 'whois'.")

if __name__ == "__main__":
    main()
