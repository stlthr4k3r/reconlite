# ReconLite

(Work in progress) A simple Python recon tool for footprinting targets.  

---

## Features

- Accepts a domain or IP address as input
- Optional WHOIS lookup (`--whois`)
- Prints raw WHOIS output for now

---

## Dependencies

- Python 3
- WHOIS command installed on your system:
  - **Linux:** `sudo apt install whois`
  - **macOS:** `brew install whois`
  - **Windows:** Install a compatible WHOIS tool or use Python alternatives

---

## Usage

```bash
# Basic usage
python3 reconlite.py example.com

# Run WHOIS lookup
python3 reconlite.py example.com --whois
