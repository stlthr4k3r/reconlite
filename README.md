# ReconLite

A simple Python recon tool for footprinting targets.

---

## Features

### WHOIS Lookup
- Native WHOIS via raw TCP sockets (port 43), no subprocess or external dependencies
- Automatic server discovery through IANA root WHOIS
- RDAP fallback for TLDs without WHOIS (Google TLDs like .app, .dev, .page)
- WHOIS referral chasing for accurate results
- IP WHOIS via ARIN with automatic RIR referral (APNIC, RIPE, LACNIC, AfriNIC)
- Cross-platform (Linux, macOS, Windows)

---

## Usage

```
python3 reconlite.py <target> --whois
```

Example:

```
$ python3 reconlite.py google.com --whois

[+] Running WHOIS for google.com...

Domain Name: google.com
Registry Domain ID: 2138514_DOMAIN_COM-VRSN
Registrar WHOIS Server: whois.markmonitor.com
Registrar URL: http://www.markmonitor.com
Updated Date: 2024-08-02T02:17:33+0000
Creation Date: 1997-09-15T07:00:00+0000
Registrar: MarkMonitor, Inc.
...
```

Works with any TLD and IP addresses:

```
$ python3 reconlite.py google.app --whois    # RDAP (Google TLD)
$ python3 reconlite.py google.fr --whois     # WHOIS (.fr)
$ python3 reconlite.py google.au --whois     # WHOIS (.au)
$ python3 reconlite.py 8.8.8.8 --whois       # IP via ARIN -> Google
$ python3 reconlite.py 1.1.1.1 --whois       # IP via ARIN -> APNIC -> Cloudflare
```

## Why not subprocess or existing libraries?

| Feature | `whois` CLI | `python-whois` | `whois` (joepie91) | `ipwhois` | **reconlite** |
|---|---|---|---|---|---|
| Domain WHOIS | Yes | Yes | Yes | No (IP only) | **Yes** |
| IP WHOIS | Yes | No | No | Yes | **Yes** |
| .app / .dev / .page | No | No | No | N/A | **Yes (RDAP)** |
| RDAP fallback | No | No | No | Yes (IP only) | **Yes** |
| Cross-platform | No (Linux/Mac) | Yes | Partial | Yes | **Yes** |
| External dependencies | System binary | python-dateutil | None | dnspython, defusedxml | **None** |

Both the system `whois` command and Python libraries fail on newer gTLDs that don't have a traditional WHOIS server:

```
$ whois google.app
getaddrinfo(whois.nic.app): Name or service not known
```

```python
>>> import whois
>>> whois.whois("google.app")
# Error trying to connect to socket: Name or service not known
```

ICANN sunsetted WHOIS in January 2025 and 374 gTLDs have already shut off port 43. RDAP is the replacement. ReconLite handles both protocols automatically via the IANA bootstrap registry, no hardcoded server lists needed.

## Requirements

- Python 3.8+
- No external dependencies

## Disclaimer

For approved penetration testing and educational purposes only. Don't fuck around and find out.
