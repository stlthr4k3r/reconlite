import argparse
import json
import re
import socket
import urllib.request

IANA_HOST = "whois.iana.org"
WHOIS_PORT = 43
TIMEOUT = 10


def whois_query(server, query, timeout=TIMEOUT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        s.connect((server, WHOIS_PORT))
        s.sendall(f"{query}\r\n".encode())
        chunks = []
        while data := s.recv(4096):
            chunks.append(data)
    return b"".join(chunks).decode("utf-8", errors="replace")


def find_whois_server(tld):
    response = whois_query(IANA_HOST, tld)

    match = re.search(r"whois:\s+(\S+)", response)
    if match:
        return match.group(1), "whois"

    if re.search(r"remarks:\s+https?://", response):
        return None, "rdap"

    server = f"whois.nic.{tld}"
    try:
        socket.getaddrinfo(server, WHOIS_PORT)
    except socket.gaierror:
        return None, None
    return server, "whois"


def find_rdap_server(tld):
    resp = urllib.request.urlopen(
        "https://data.iana.org/rdap/dns.json", timeout=TIMEOUT
    )
    data = json.loads(resp.read())
    for tlds, urls in data.get("services", []):
        if tld in tlds:
            return urls[0]
    return None


def rdap_lookup(domain):
    tld = domain.rsplit(".", 1)[-1]
    base_url = find_rdap_server(tld)
    if not base_url:
        return None

    req = urllib.request.Request(
        f"{base_url}domain/{domain}",
        headers={"Accept": "application/rdap+json"},
    )
    resp = urllib.request.urlopen(req, timeout=TIMEOUT)
    data = json.loads(resp.read())

    registrar = None
    for entity in data.get("entities", []):
        if "registrar" not in entity.get("roles", []):
            continue
        for field in entity.get("vcardArray", [None, []])[1]:
            if field[0] == "fn":
                registrar = field[3]
                break
        break

    events = {e["eventAction"]: e["eventDate"] for e in data.get("events", [])}
    name_servers = [ns.get("ldhName", "") for ns in data.get("nameservers", [])]

    lines = [f"Domain Name: {domain.upper()}"]
    if registrar:
        lines.append(f"Registrar: {registrar}")
    if events.get("registration"):
        lines.append(f"Creation Date: {events['registration']}")
    if events.get("expiration"):
        lines.append(f"Expiry Date: {events['expiration']}")
    lines.extend(f"Status: {s}" for s in data.get("status", []))
    lines.extend(f"Name Server: {ns}" for ns in name_servers)
    lines.append(f"\nSource: RDAP ({base_url})")

    return "\n".join(lines)


def whois_lookup(domain):
    tld = domain.rsplit(".", 1)[-1]
    server, method = find_whois_server(tld)

    if method == "rdap" or not server:
        result = rdap_lookup(domain)
        if result:
            return result, None
        return None, "No WHOIS/RDAP server found for this TLD"

    try:
        response = whois_query(server, domain)
    except (socket.gaierror, socket.timeout, OSError):
        result = rdap_lookup(domain)
        if result:
            return result, None
        return None, f"WHOIS server {server} unreachable and RDAP failed"

    referral = re.search(r"Whois Server:\s*(\S+)", response, re.IGNORECASE)
    if not referral:
        return response, None

    try:
        return whois_query(referral.group(1), domain), None
    except (socket.gaierror, socket.timeout, OSError):
        return response, None


def main():
    parser = argparse.ArgumentParser(description="ReconLite - Simple Recon Tool")
    parser.add_argument("target", help="Target domain")
    parser.add_argument("--whois", action="store_true", help="Run WHOIS lookup")
    args = parser.parse_args()

    if not args.whois:
        parser.print_help()
        return

    print(f"\n[+] Running WHOIS for {args.target}...\n")
    result, error = whois_lookup(args.target)

    if error:
        print(f"[-] {error}")
        return

    print(result)


if __name__ == "__main__":
    main()
