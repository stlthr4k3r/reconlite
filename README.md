# ReconLite

A simple Python recon tool for footprinting targets.

---

## Features

### WHOIS Lookup
- Extracts **Registrar**, **Creation Date**, and **Name Servers**  
- Handles multiple name servers  
- Case-insensitive parsing with fallback labels  

### Modular Design
- `parse_whois()` handles extraction  
- `print_whois()` prints results neatly  

---

## Usage

Run ReconLite with WHOIS lookup:

```bash
python3 reconlite.py <target> --whois

Example:

python3 reconlite.py example.com --whois

Expected output:

[+] WHOIS Summary:
    Registrar: GoDaddy
    Creation Date: 2020-01-01
    Name Servers:
        - ns1.example.com
        - ns2.example.com
```

## Disclaimer

For approved penetration testing and educational purposes only. Don't fuck around and find out.
