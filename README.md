# ReconLite

A simple Python recon tool for footprinting targets.

---

## Features

### WHOIS Lookup
- Native WHOIS via raw TCP sockets (port 43), no subprocess or external dependencies
- Automatic server discovery through IANA root WHOIS
- RDAP fallback for TLDs without WHOIS (Google TLDs like .app, .dev, .page)
- WHOIS referral chasing for accurate results
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

Works with any TLD:

```
$ python3 reconlite.py google.app --whois    # RDAP (Google TLD)
$ python3 reconlite.py google.fr --whois     # WHOIS (.fr)
$ python3 reconlite.py google.au --whois     # WHOIS (.au)
```

## Why not subprocess or python-whois?

Both the system `whois` command and the `python-whois` library fail on newer gTLDs that don't have a traditional WHOIS server (like .app, .dev, .page):

```
$ whois google.app
getaddrinfo(whois.nic.app): Name or service not known
```

```python
>>> import whois
>>> whois.whois("google.app")
# Error trying to connect to socket: Name or service not known
```

ReconLite handles these automatically via RDAP fallback through the IANA bootstrap registry, no hardcoded server lists needed.

## Requirements

- Python 3.8+
- No external dependencies

## Disclaimer

For approved penetration testing and educational purposes only. Don't fuck around and find out.
