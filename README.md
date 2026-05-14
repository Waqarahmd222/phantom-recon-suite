<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Platform-Windows%20|%20Linux%20|%20macOS-0891b2?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Dependencies-None-00ff88?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-f59e0b?style=for-the-badge" />
</p>

<h1 align="center">⚡ Phantom Recon Suite v2.0</h1>

<p align="center">
  <strong>A zero-dependency reconnaissance & footprinting toolkit built entirely with Python 3 stdlib.</strong><br>
  Designed for CEH / eJPT exam preparation, cybersecurity students, and authorized penetration testing.
</p>

<p align="center">
  <img src="screenshots/phantom_recon_main.png" alt="Phantom Recon Suite Screenshot" width="850"/>
</p>

---

## Why Phantom Recon Suite?

Most recon tools require installing dozens of packages or rely on external APIs with paid keys. Phantom Recon Suite does everything with **zero pip installs** — just Python 3 and its standard library. It's a single-file, portable toolkit you can run anywhere.

---

## Features

### 🔍 9 Reconnaissance Modules

| Module | What It Does |
|--------|-------------|
| **DNS Lookup** | Enumerates A, AAAA, MX, NS, CNAME, TXT, SOA records with reverse DNS cross-verification |
| **WHOIS / RDAP** | Domain registration data via RDAP with multiple fallback sources |
| **Port Scanner** | TCP connect scan with inline banner grabbing and service detection across 50+ known ports |
| **Traceroute** | Network path tracing with color-coded hop visualization |
| **Banner Grabber** | Protocol-aware banner grabbing with SSL/TLS support for service fingerprinting |
| **SSL/TLS Analyzer** | Full certificate analysis — issuer, expiry, SANs, cipher suite, trust verification |
| **GeoIP Intel** | Multi-source IP geolocation with cross-verification, ISP, ASN, proxy/VPN detection |
| **Subdomain Finder** | DNS brute-force enumeration using 85+ common subdomain prefixes |
| **Network Info** | Local host intelligence — interfaces, public IP, ISP, routing table summary |

### 🎨 Professional UI
- Dark cyberpunk-themed interface built with Tkinter
- Animated splash screen on launch
- Color-coded output with section headers and result tables
- Live clock and pulsing status indicator
- Focus-glow effects on input fields

### ⚙️ Workflow Features
- **Enter key** triggers scans — no mouse clicking needed
- **Stop button** on every tab to cancel long-running scans
- **PDF report export** — generates multi-page professional reports (zero dependencies, raw PDF)
- **Copy All** — one-click clipboard copy of all scan results
- Cross-platform: Windows, Linux, macOS

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/phantom-recon-suite.git
cd phantom-recon-suite

# Run it (no installation needed)
python phantom_recon.py
```

**Requirements:** Python 3.7+ with Tkinter (included by default on Windows and macOS).

On Linux, if Tkinter is missing:
```bash
# Ubuntu / Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

---

## Screenshots

<details>
<summary><strong>Click to expand screenshots</strong></summary>

### DNS Lookup
![DNS Lookup](screenshots/dns_lookup.png)

### Port Scanner
![Port Scanner](screenshots/port_scan.png)

### SSL/TLS Analysis
![SSL Analysis](screenshots/ssl_analysis.png)

### PDF Report Export
![PDF Report](screenshots/pdf_report.png)

</details>

---

## How It Works

Phantom Recon Suite uses only Python standard library modules:

- `socket` — DNS resolution, port scanning, banner grabbing
- `ssl` — TLS certificate retrieval and cipher analysis
- `subprocess` — System command integration (nslookup, dig, traceroute)
- `urllib` — RDAP/WHOIS queries, GeoIP API calls (ip-api.com, ipinfo.io)
- `tkinter` — Complete GUI with tabbed interface
- `threading` — Non-blocking scan execution with stop support
- `json` — API response parsing

No external packages. No API keys. No pip install.

---

## PDF Report

The tool generates professional PDF reports from raw PDF format — no ReportLab, no FPDF, no dependencies at all. Reports include:

- Title page with target and timestamp
- All scan results organized by module
- Proper pagination with headers and footers
- Word-wrapped content for readability

---

## Project Structure

```
phantom-recon-suite/
├── phantom_recon.py      # Single-file application (entire toolkit)
├── README.md             # This file
├── LICENSE               # MIT License
└── screenshots/          # UI screenshots for README
    ├── phantom_recon_main.png
    ├── dns_lookup.png
    ├── port_scan.png
    ├── ssl_analysis.png
    └── pdf_report.png
```

---

## Disclaimer

> **⚠️ This tool is for EDUCATIONAL PURPOSES and AUTHORIZED TESTING ONLY.**
>
> Scanning networks or systems without explicit written permission is **illegal** under the Computer Fraud and Abuse Act (CFAA) and equivalent laws worldwide. Always obtain proper authorization before performing any reconnaissance.
>
> The author assumes no liability for misuse of this tool.

---

## Use Cases

- **CEH / eJPT Exam Preparation** — Practice footprinting and reconnaissance techniques
- **Cybersecurity Lab Work** — Hands-on labs for networking and security courses
- **Authorized Penetration Testing** — Quick initial recon during engagements
- **Network Troubleshooting** — DNS debugging, SSL certificate checks, port verification

---

## Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-module`)
3. Commit your changes (`git commit -m 'Add new recon module'`)
4. Push to the branch (`git push origin feature/new-module`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## Author

**Waqar** — Cybersecurity enthusiast & CEH student

⭐ If you found this useful, please star the repo!

---

<p align="center">
  <strong>Built with ❤️ and Python stdlib only</strong>
</p>
