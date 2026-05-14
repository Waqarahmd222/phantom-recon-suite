#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║          ⚡ PHANTOM RECON SUITE v2.0                             ║
║          Footprinting & Reconnaissance Toolkit                   ║
║          For CEH Study & Ethical Penetration Testing             ║
║          Built with Python 3 stdlib only - No pip install needed ║
╚══════════════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import socket
import subprocess
import platform
import json
import urllib.request
import urllib.error
import ssl
import os
import re
import time
import ipaddress
from datetime import datetime


# ═══════════════════════ COLOUR PALETTE (Enhanced) ═════════════
BG         = "#060816"
BG2        = "#0b1023"
PANEL      = "#0f1629"
PANEL2     = "#0a0f20"
BORDER     = "#1a2744"
ACCENT     = "#00d4ff"
ACCENT2    = "#7c3aed"
ACCENT3    = "#00b4d8"
GLOW       = "#0ea5e9"
GREEN      = "#00ff88"
GREEN2     = "#22c55e"
RED        = "#ff4757"
YELLOW     = "#ffd32a"
ORANGE     = "#ff6b35"
CYAN       = "#06b6d4"
MAGENTA    = "#e879f9"
TEXT       = "#e2e8f0"
TEXT_DIM   = "#64748b"
TEXT_BRIGHT= "#f8fafc"
GOLD       = "#f59e0b"

# ═══════════════════════ FONT SIZES (BIGGER) ══════════════════
MONO       = ("Consolas", 13)
MONO_SM    = ("Consolas", 12)
MONO_LG    = ("Consolas", 14, "bold")
UI         = ("Segoe UI", 12)
UI_BOLD    = ("Segoe UI", 12, "bold")
UI_LG      = ("Segoe UI", 14, "bold")
TITLE_FONT = ("Consolas", 22, "bold")
SUB_FONT   = ("Segoe UI", 11)
TAB_FONT   = ("Segoe UI", 10)
INFO_FONT  = ("Segoe UI", 10)
FOOTER_FONT= ("Segoe UI", 9)
HEADER_FONT= ("Consolas", 15, "bold")
STATUS_FONT= ("Consolas", 13, "bold")
ENTRY_FONT = ("Consolas", 13)
LABEL_FONT = ("Segoe UI", 12)
BTN_FONT   = ("Segoe UI", 11, "bold")
BTN_COLOR  = "#0891b2"
BTN_HOVER  = "#06b6d4"
BTN_ACTIVE = "#22d3ee"


# ═══════════════════════ HELPER FUNCTIONS ══════════════════════
def now():
    return datetime.now().strftime("%H:%M:%S")

def log(w, msg, color=TEXT):
    w.config(state=tk.NORMAL)
    tag = f"tag_{color.replace('#','')}"
    w.tag_config(tag, foreground=color)
    w.insert(tk.END, f"[{now()}]  {msg}\n", tag)
    w.see(tk.END)
    w.config(state=tk.DISABLED)

def log_section(w, title):
    w.config(state=tk.NORMAL)
    divider = "━" * 60
    w.insert(tk.END, f"\n{divider}\n", "divider")
    w.tag_config("divider", foreground=ACCENT3)
    w.insert(tk.END, f"  ◆  {title}\n", "section_title")
    w.tag_config("section_title", foreground=ACCENT, font=MONO_LG)
    w.insert(tk.END, f"{divider}\n\n", "divider")
    w.see(tk.END)
    w.config(state=tk.DISABLED)

def log_subsection(w, title):
    w.config(state=tk.NORMAL)
    w.insert(tk.END, f"\n  ┌── {title} ──┐\n", "subsection")
    w.tag_config("subsection", foreground=YELLOW, font=("Consolas", 13, "bold"))
    w.see(tk.END)
    w.config(state=tk.DISABLED)

def clear(w):
    w.config(state=tk.NORMAL)
    w.delete(1.0, tk.END)
    w.config(state=tk.DISABLED)

stop_event = threading.Event()

def thread(fn, *args):
    stop_event.clear()
    threading.Thread(target=fn, args=args, daemon=True).start()

def make_output(parent, height=20):
    # Container with subtle border glow
    container = tk.Frame(parent, bg=ACCENT3, padx=1, pady=1)
    container.pack(fill=tk.BOTH, expand=True, padx=14, pady=(0, 12))

    txt = scrolledtext.ScrolledText(
        container, height=height, bg=PANEL2, fg=TEXT,
        font=MONO, insertbackground=ACCENT,
        relief=tk.FLAT, borderwidth=0,
        selectbackground=ACCENT2,
        selectforeground=TEXT_BRIGHT,
        state=tk.DISABLED,
        padx=12, pady=10,
        wrap=tk.WORD
    )
    txt.pack(fill=tk.BOTH, expand=True)
    return txt

def make_entry(parent, label_text, width=40):
    row = tk.Frame(parent, bg=BG)
    row.pack(fill=tk.X, padx=14, pady=5)
    tk.Label(row, text=label_text, bg=BG, fg=CYAN, font=LABEL_FONT,
             width=20, anchor="w").pack(side=tk.LEFT)

    # Entry with glowing border
    entry_frame = tk.Frame(row, bg=ACCENT3, padx=1, pady=1)
    entry_frame.pack(side=tk.LEFT, padx=(0, 8))

    e = tk.Entry(entry_frame, width=width, bg=PANEL, fg=TEXT_BRIGHT, font=ENTRY_FONT,
                 insertbackground=ACCENT, relief=tk.FLAT,
                 highlightthickness=0)
    e.pack(ipady=6, padx=0)

    # Focus glow effect
    def on_focus_in(event):
        entry_frame.configure(bg=ACCENT)
    def on_focus_out(event):
        entry_frame.configure(bg=ACCENT3)
    e.bind("<FocusIn>", on_focus_in)
    e.bind("<FocusOut>", on_focus_out)

    return e

def fancy_button(parent, text, command, color=None, is_primary=True):
    """Modern capsule-shaped button with glow hover effect"""
    if color is None:
        color = BTN_COLOR if is_primary else PANEL

    btn_bg = color if is_primary else PANEL
    btn_fg = "#ffffff" if is_primary else TEXT_DIM

    # Outer frame acts as the pill border/glow
    outer = tk.Frame(parent, bg=ACCENT3 if is_primary else BORDER,
                     padx=1, pady=1)
    outer.pack(side=tk.LEFT, padx=6, pady=8)

    b = tk.Button(
        outer, text=f"  {text}  ", command=command,
        bg=btn_bg, fg=btn_fg, font=BTN_FONT,
        relief=tk.FLAT, cursor="hand2",
        activebackground=ACCENT, activeforeground="#000000",
        pady=7, bd=0,
        highlightthickness=0,
    )
    b.pack(fill=tk.BOTH, expand=True)

    # Hover animation with glow
    def on_enter(e):
        if is_primary:
            b.configure(bg=BTN_HOVER, fg="#000000")
            outer.configure(bg=ACCENT)
        else:
            b.configure(bg=BORDER, fg=ACCENT)
            outer.configure(bg=ACCENT3)
    def on_leave(e):
        b.configure(bg=btn_bg, fg=btn_fg)
        outer.configure(bg=ACCENT3 if is_primary else BORDER)

    b.bind("<Enter>", on_enter)
    b.bind("<Leave>", on_leave)
    return b

def get_target(entry_widget, output_widget):
    val = entry_widget.get().strip()
    if not val:
        messagebox.showwarning("⚠ Input Missing", "Please enter a target domain or IP address.")
        return None
    return val

def is_stopped():
    """Check if user requested scan stop."""
    return stop_event.is_set()

def stop_scan():
    """Signal all running scans to stop."""
    stop_event.set()


# ═══════════════════════ ACCURATE RECON FUNCTIONS ══════════════

# ── 1. DNS Lookup (Enhanced Accuracy) ─────────────────────────
def dns_lookup(target, out):
    clear(out)
    log_section(out, f"DNS LOOKUP  ►  {target}")
    log(out, "⏳ Starting comprehensive DNS enumeration...", YELLOW)

    record_types = {
        "A":     "IPv4 Address",
        "AAAA":  "IPv6 Address",
        "MX":    "Mail Exchange Server",
        "NS":    "Authoritative Nameserver",
        "CNAME": "Canonical Name (Alias)",
        "TXT":   "TXT Record (SPF/DKIM/etc)",
        "SOA":   "Start of Authority",
    }

    # Step 1: Primary A record via socket (cross-verified)
    log_subsection(out, "PRIMARY RESOLUTION")
    resolved_ip = None
    try:
        ip = socket.gethostbyname(target)
        resolved_ip = ip
        log(out, f"  ✔  A Record (socket)   ►  {ip}", GREEN)

        # Verify with reverse DNS
        try:
            rev = socket.gethostbyaddr(ip)
            log(out, f"  ✔  Reverse DNS (PTR)   ►  {rev[0]}", CYAN)
        except Exception:
            log(out, f"  ℹ  Reverse DNS (PTR)   ►  No PTR record", TEXT_DIM)
    except socket.gaierror as e:
        log(out, f"  ✘  A Record            ►  Could not resolve: {e}", RED)
    except Exception as e:
        log(out, f"  ✘  A Record            ►  Error: {e}", RED)

    # Step 2: Detailed record enumeration via nslookup/dig
    log_subsection(out, "RECORD ENUMERATION")
    for rtype, rdesc in record_types.items():
        if is_stopped():
            log(out, "\n  ⛔  DNS lookup stopped by user.", ORANGE)
            break
        try:
            if platform.system() == "Windows":
                cmd = ["nslookup", f"-type={rtype}", target]
            else:
                cmd = ["dig", "+short", "+time=5", "+tries=2", rtype, target]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10,
                                    creationflags=0x08000000 if platform.system() == "Windows" else 0)
            output = result.stdout.strip()

            if not output or "NXDOMAIN" in output or "can't find" in output.lower():
                log(out, f"  ─  {rtype:<8} [{rdesc}]  ►  No record found", TEXT_DIM)
                continue

            # Parse Windows nslookup output more accurately
            if platform.system() == "Windows":
                lines = output.splitlines()
                relevant_lines = []
                in_answer = False

                for line in lines:
                    line_stripped = line.strip()
                    if not line_stripped:
                        continue
                    # Skip header lines (server info)
                    if line_stripped.startswith("Server:") or line_stripped.startswith("Address:") and not in_answer:
                        if line_stripped.startswith("Address:"):
                            in_answer = True
                        continue
                    if line_stripped.startswith("Non-authoritative"):
                        in_answer = True
                        continue

                    # Extract actual data
                    if in_answer and line_stripped:
                        # Clean up common nslookup output patterns
                        if "=" in line_stripped:
                            parts = line_stripped.split("=", 1)
                            value = parts[1].strip()
                            label = parts[0].strip().lower()
                            if rtype == "MX" and "mail exchanger" in label:
                                relevant_lines.append(f"Priority {value}")
                            elif rtype == "NS" and "nameserver" in label:
                                relevant_lines.append(value)
                            elif rtype == "TXT":
                                relevant_lines.append(value.strip('"'))
                            elif rtype == "SOA":
                                relevant_lines.append(value)
                            else:
                                relevant_lines.append(value)
                        elif ":" in line_stripped:
                            parts = line_stripped.split(":", 1)
                            value = parts[1].strip()
                            if value:
                                relevant_lines.append(value)
                        elif rtype in ("A", "AAAA"):
                            # Check if it looks like an IP
                            if re.match(r'^[\d\.:a-fA-F]+$', line_stripped):
                                relevant_lines.append(line_stripped)
                        else:
                            relevant_lines.append(line_stripped)

                for rl in relevant_lines:
                    if rl and len(rl) > 1:
                        log(out, f"  ✔  {rtype:<8} [{rdesc}]  ►  {rl}", GREEN2)
            else:
                # Linux/Mac dig output is cleaner
                for line in output.splitlines():
                    line = line.strip()
                    if line and not line.startswith(";"):
                        log(out, f"  ✔  {rtype:<8} [{rdesc}]  ►  {line}", GREEN2)

        except subprocess.TimeoutExpired:
            log(out, f"  ⏱  {rtype:<8} [{rdesc}]  ►  Query timed out", ORANGE)
        except Exception as e:
            log(out, f"  ✘  {rtype:<8}  ►  Error: {e}", RED)

    # Step 3: All resolved IPs (complete list)
    log_subsection(out, "ALL RESOLVED ADDRESSES")
    try:
        all_info = socket.getaddrinfo(target, None)
        ipv4s = sorted(set(r[4][0] for r in all_info if r[0] == socket.AF_INET))
        ipv6s = sorted(set(r[4][0] for r in all_info if r[0] == socket.AF_INET6))

        if ipv4s:
            for ip in ipv4s:
                log(out, f"  ✔  IPv4  ►  {ip}", ACCENT)
        if ipv6s:
            for ip in ipv6s:
                log(out, f"  ✔  IPv6  ►  {ip}", CYAN)
        if not ipv4s and not ipv6s:
            log(out, f"  ─  No additional addresses found", TEXT_DIM)
    except Exception:
        pass

    log(out, f"\n{'━'*60}", ACCENT3)
    log(out, "✔  DNS Lookup Complete — All records enumerated.", GREEN)


# ── 2. WHOIS (Enhanced with multiple fallbacks) ───────────────
def whois_lookup(target, out):
    clear(out)
    log_section(out, f"WHOIS  ►  {target}")
    log(out, "⏳ Querying WHOIS / RDAP databases...", YELLOW)

    domain = target.replace("http://", "").replace("https://", "").split("/")[0]

    # Try system whois first (Linux/Mac)
    try:
        if platform.system() != "Windows":
            result = subprocess.run(["whois", domain], capture_output=True, text=True, timeout=15)
            if result.stdout and len(result.stdout) > 100:
                log_subsection(out, "SYSTEM WHOIS RESULT")
                important_keys = [
                    "domain name", "registrar", "registrant", "admin", "tech",
                    "creation", "created", "updated", "modified", "expir",
                    "name server", "nameserver", "status", "dnssec",
                    "country", "email", "phone", "org", "registry",
                    "registrar url", "abuse"
                ]
                for line in result.stdout.splitlines():
                    line_lower = line.lower().strip()
                    if any(k in line_lower for k in important_keys):
                        line_clean = line.strip()
                        if ":" in line_clean:
                            key, val = line_clean.split(":", 1)
                            log(out, f"  {key.strip():<30} ►  {val.strip()}", TEXT)
                        else:
                            log(out, f"  {line_clean}", TEXT)
                log(out, "\n✔  WHOIS Complete.", GREEN)
                return
    except Exception:
        pass

    # RDAP Lookup - Primary method for Windows and fallback
    rdap_urls = [
        f"https://rdap.org/domain/{domain}",
        f"https://rdap.verisign.com/com/v1/domain/{domain}",
    ]

    for url in rdap_urls:
        try:
            ctx = ssl.create_default_context()
            req = urllib.request.Request(url, headers={
                "User-Agent": "PhantomRecon/2.0",
                "Accept": "application/rdap+json, application/json"
            })
            with urllib.request.urlopen(req, context=ctx, timeout=12) as resp:
                data = json.loads(resp.read().decode())

            log_subsection(out, "DOMAIN REGISTRATION")
            log(out, f"  Domain Name      ►  {data.get('ldhName', domain)}", GREEN)
            log(out, f"  Handle           ►  {data.get('handle', 'N/A')}", TEXT)

            # Status
            statuses = data.get("status", [])
            if statuses:
                for st in statuses:
                    log(out, f"  Status           ►  {st}", CYAN)

            # Events (dates)
            log_subsection(out, "IMPORTANT DATES")
            for event in data.get("events", []):
                act = event.get("eventAction", "")
                dt = event.get("eventDate", "")
                if act and dt:
                    # Format date nicely
                    try:
                        parsed = datetime.fromisoformat(dt.replace("Z", "+00:00"))
                        dt_str = parsed.strftime("%Y-%m-%d %H:%M:%S UTC")
                    except Exception:
                        dt_str = dt[:19]
                    log(out, f"  {act.capitalize():<22} ►  {dt_str}", TEXT)

            # Nameservers
            ns_list = data.get("nameservers", [])
            if ns_list:
                log_subsection(out, f"NAMESERVERS ({len(ns_list)})")
                for ns in ns_list:
                    ns_name = ns.get("ldhName", "")
                    if ns_name:
                        log(out, f"  NS  ►  {ns_name}", ACCENT)

            # Entities (registrant, admin, tech)
            entities = data.get("entities", [])
            if entities:
                log_subsection(out, "CONTACT ENTITIES")
                for ent in entities:
                    roles = ", ".join(ent.get("roles", []))
                    if roles:
                        log(out, f"\n  ── Role: {roles.upper()} ──", YELLOW)

                    vcard = ent.get("vcardArray", [])
                    if vcard and len(vcard) > 1:
                        for item in vcard[1]:
                            if isinstance(item, list) and len(item) >= 4:
                                key = item[0]
                                val = item[3]
                                if key in ("fn", "email", "tel", "org", "adr"):
                                    if isinstance(val, list):
                                        val = " ".join(str(v) for v in val if v)
                                    if val and str(val).strip():
                                        log(out, f"  {key.upper():<22} ►  {val}", TEXT)

                    # Sub-entities
                    for sub_ent in ent.get("entities", []):
                        sub_roles = ", ".join(sub_ent.get("roles", []))
                        sub_vcard = sub_ent.get("vcardArray", [])
                        if sub_vcard and len(sub_vcard) > 1:
                            log(out, f"\n  ── Sub-Role: {sub_roles.upper()} ──", GOLD)
                            for item in sub_vcard[1]:
                                if isinstance(item, list) and len(item) >= 4:
                                    key = item[0]
                                    val = item[3]
                                    if key in ("fn", "email", "tel", "org"):
                                        if isinstance(val, list):
                                            val = " ".join(str(v) for v in val if v)
                                        if val and str(val).strip():
                                            log(out, f"  {key.upper():<22} ►  {val}", TEXT)

            log(out, f"\n{'━'*60}", ACCENT3)
            log(out, "✔  WHOIS/RDAP Complete — Full registration data retrieved.", GREEN)
            return

        except urllib.error.HTTPError as e:
            log(out, f"  ℹ  RDAP source {url.split('/')[2]}: HTTP {e.code}", TEXT_DIM)
            continue
        except Exception as e:
            log(out, f"  ℹ  RDAP source failed: {e}", TEXT_DIM)
            continue

    log(out, "  ✘  Could not retrieve WHOIS data from any source.", RED)
    log(out, "  💡 Tip: Try common TLDs (.com, .net, .org). Some TLDs have limited RDAP.", YELLOW)


# ── 3. Port Scanner (Enhanced with service detection) ─────────
COMMON_PORTS = {
    20:"FTP-Data", 21:"FTP", 22:"SSH", 23:"Telnet", 25:"SMTP",
    53:"DNS", 67:"DHCP-S", 68:"DHCP-C", 69:"TFTP", 80:"HTTP",
    110:"POP3", 111:"RPC", 119:"NNTP", 123:"NTP", 135:"MSRPC",
    137:"NetBIOS-NS", 138:"NetBIOS-DG", 139:"NetBIOS-SS",
    143:"IMAP", 161:"SNMP", 162:"SNMP-Trap",
    389:"LDAP", 443:"HTTPS", 445:"SMB", 465:"SMTPS",
    514:"Syslog", 587:"SMTP-Sub", 636:"LDAPS",
    993:"IMAPS", 995:"POP3S", 1433:"MSSQL", 1434:"MSSQL-B",
    1521:"Oracle", 1723:"PPTP", 2049:"NFS",
    3306:"MySQL", 3389:"RDP", 5432:"PostgreSQL",
    5900:"VNC", 5985:"WinRM", 5986:"WinRM-S",
    6379:"Redis", 6667:"IRC", 8080:"HTTP-Alt", 8443:"HTTPS-Alt",
    9090:"WebConsole", 9200:"Elasticsearch", 27017:"MongoDB",
    27018:"MongoDB-S", 5601:"Kibana",
}

def port_scan(target, port_range, out):
    clear(out)
    log_section(out, f"PORT SCAN  ►  {target}  |  Range: {port_range}")
    log(out, "⏳ Resolving target...", YELLOW)

    try:
        ip = socket.gethostbyname(target)
        log(out, f"  ✔  Target IP         ►  {ip}", GREEN)
    except Exception as e:
        log(out, f"  ✘  Cannot resolve {target}: {e}", RED)
        return

    # Verify IP with reverse DNS
    try:
        rev = socket.gethostbyaddr(ip)
        log(out, f"  ✔  Reverse DNS       ►  {rev[0]}", CYAN)
    except Exception:
        pass

    # Parse port range
    try:
        if "-" in port_range:
            start, end = port_range.split("-")
            ports = list(range(int(start.strip()), int(end.strip()) + 1))
        elif port_range.lower() == "top":
            ports = sorted(COMMON_PORTS.keys())
        else:
            ports = [int(p.strip()) for p in port_range.split(",")]
    except Exception:
        log(out, "  ✘  Invalid port range. Use: 1-1024 or top or 80,443,8080", RED)
        return

    total = len(ports)
    log(out, f"  ℹ  Scanning {total} ports (timeout: 1.0s per port)...", YELLOW)
    log(out, "", TEXT)

    open_ports = []
    closed = 0
    filtered = 0
    start_time = time.time()

    for i, port in enumerate(ports):
        if is_stopped():
            log(out, "\n  ⛔  Scan stopped by user.", ORANGE)
            break
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0)
            result = s.connect_ex((ip, port))

            if result == 0:
                svc = COMMON_PORTS.get(port, "Unknown")
                # Try quick banner grab for version
                banner_info = ""
                try:
                    if port in (80, 8080):
                        s.send(b"HEAD / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")
                        data = s.recv(256).decode("utf-8", errors="ignore")
                        for line in data.splitlines():
                            if line.lower().startswith("server:"):
                                banner_info = f"  ({line.split(':', 1)[1].strip()})"
                                break
                    elif port == 22:
                        data = s.recv(256).decode("utf-8", errors="ignore").strip()
                        if data:
                            banner_info = f"  ({data.split(chr(10))[0][:50]})"
                except Exception:
                    pass

                s.close()
                log(out, f"  ✔  PORT {port:<6}  OPEN    [{svc}]{banner_info}", GREEN)
                open_ports.append((port, svc))
            else:
                s.close()
                closed += 1
        except socket.timeout:
            filtered += 1
        except Exception:
            closed += 1

    elapsed = time.time() - start_time

    # Summary
    log(out, "", TEXT)
    log_subsection(out, "SCAN SUMMARY")
    log(out, f"  ✔  Open Ports        ►  {len(open_ports)}", GREEN if open_ports else YELLOW)
    log(out, f"  ✘  Closed Ports      ►  {closed}", TEXT)
    log(out, f"  ⚡ Filtered Ports    ►  {filtered}", ORANGE if filtered else TEXT)
    log(out, f"  ⏱  Scan Duration     ►  {elapsed:.1f} seconds", CYAN)

    if open_ports:
        log(out, "", TEXT)
        log(out, "  ┌─────────────────────────────────────────┐", ACCENT3)
        log(out, "  │  PORT    STATE    SERVICE                │", ACCENT)
        log(out, "  ├─────────────────────────────────────────┤", ACCENT3)
        for port, svc in open_ports:
            log(out, f"  │  {port:<8}OPEN     {svc:<23}│", GREEN)
        log(out, "  └─────────────────────────────────────────┘", ACCENT3)

    log(out, f"\n{'━'*60}", ACCENT3)
    log(out, f"✔  Port Scan Complete. {len(open_ports)} open port(s) found.", GREEN if open_ports else YELLOW)


# ── 4. Traceroute ──────────────────────────────────────────────
def traceroute(target, out):
    clear(out)
    log_section(out, f"TRACEROUTE  ►  {target}")
    log(out, "⏳ Tracing network path...\n", YELLOW)

    try:
        ip = socket.gethostbyname(target)
        log(out, f"  ✔  Target IP  ►  {ip}\n", ACCENT)
    except Exception:
        pass

    try:
        if platform.system() == "Windows":
            cmd = ["tracert", "-d", "-h", "30", target]
        else:
            cmd = ["traceroute", "-m", "30", "-n", target]

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, text=True,
                                   creationflags=0x08000000 if platform.system() == "Windows" else 0)
        hop = 0
        for line in process.stdout:
            if is_stopped():
                process.kill()
                log(out, "\n  ⛔  Traceroute stopped by user.", ORANGE)
                break
            line = line.strip()
            if not line:
                continue
            hop += 1
            # Color by hop distance with gradient
            if hop <= 5:
                color = GREEN
            elif hop <= 10:
                color = GREEN2
            elif hop <= 15:
                color = YELLOW
            elif hop <= 20:
                color = ORANGE
            else:
                color = RED
            log(out, f"  {line}", color)

        process.wait()
        log(out, f"\n{'━'*60}", ACCENT3)
        log(out, f"✔  Traceroute Complete — {hop} hops traced.", GREEN)

    except FileNotFoundError:
        log(out, "  ✘  tracert/traceroute not found on this system.", RED)
    except Exception as e:
        log(out, f"  ✘  Error: {e}", RED)


# ── 5. Banner Grabber (Enhanced probes) ───────────────────────
SERVICE_PROBES = {
    21:  (b"", 3),           # FTP sends banner on connect
    22:  (b"", 3),           # SSH sends banner on connect
    23:  (b"", 3),           # Telnet sends banner
    25:  (b"EHLO phantom\r\n", 3),
    80:  (b"HEAD / HTTP/1.1\r\nHost: {host}\r\nUser-Agent: PhantomRecon/2.0\r\nConnection: close\r\n\r\n", 4),
    110: (b"", 3),           # POP3 banner
    143: (b"", 3),           # IMAP banner
    443: (b"HEAD / HTTP/1.1\r\nHost: {host}\r\nUser-Agent: PhantomRecon/2.0\r\nConnection: close\r\n\r\n", 4),
    3306:(b"", 3),           # MySQL banner
    3389:(b"", 2),           # RDP
    8080:(b"HEAD / HTTP/1.1\r\nHost: {host}\r\nUser-Agent: PhantomRecon/2.0\r\nConnection: close\r\n\r\n", 4),
    8443:(b"HEAD / HTTP/1.1\r\nHost: {host}\r\nUser-Agent: PhantomRecon/2.0\r\nConnection: close\r\n\r\n", 4),
}

def banner_grab(target, ports_str, out):
    clear(out)
    log_section(out, f"BANNER GRABBER  ►  {target}")
    log(out, "⏳ Grabbing service banners with targeted probes...\n", YELLOW)

    try:
        ip = socket.gethostbyname(target)
        log(out, f"  ✔  Resolved IP  ►  {ip}\n", ACCENT)
    except Exception:
        log(out, "  ✘  Cannot resolve target.", RED)
        return

    try:
        ports = [int(p.strip()) for p in ports_str.split(",")]
    except Exception:
        ports = [21, 22, 23, 25, 80, 110, 143, 443, 3306, 8080]

    grabbed = 0
    for port in ports:
        if is_stopped():
            log(out, "\n  ⛔  Banner grab stopped by user.", ORANGE)
            break
        try:
            s = socket.socket()
            s.settimeout(4)
            s.connect((ip, port))

            probe_data, recv_size_kb = SERVICE_PROBES.get(port, (b"", 2))
            probe = probe_data.replace(b"{host}", target.encode())

            use_ssl = port in (443, 8443, 993, 995, 465)

            if use_ssl:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)

            banner = b""
            try:
                if probe:
                    s.send(probe)
                    time.sleep(0.3)
                banner = s.recv(recv_size_kb * 1024)
            except Exception:
                pass

            # If no banner with probe, try receiving without sending
            if not banner:
                try:
                    banner = s.recv(1024)
                except Exception:
                    pass

            s.close()

            if banner:
                decoded = banner.decode("utf-8", errors="ignore").strip()
                lines = decoded.splitlines()[:8]
                log(out, f"  ┌── PORT {port} {'─'*40}", ACCENT)
                svc = COMMON_PORTS.get(port, "Unknown")
                log(out, f"  │  Service: {svc}", CYAN)
                for l in lines:
                    l = l.strip()
                    if l:
                        # Highlight headers
                        if ":" in l and any(h in l.lower() for h in ["server:", "x-powered", "content-type", "http/"]):
                            log(out, f"  │  ⚡ {l}", GREEN)
                        else:
                            log(out, f"  │  {l}", TEXT)
                log(out, f"  └{'─'*50}", ACCENT3)
                grabbed += 1
            else:
                log(out, f"  ─  PORT {port}  ►  Connected but no banner returned", TEXT_DIM)

        except ConnectionRefusedError:
            log(out, f"  ✘  PORT {port}  ►  Connection Refused (Closed)", RED)
        except socket.timeout:
            log(out, f"  ⏱  PORT {port}  ►  Connection Timed Out (Filtered)", ORANGE)
        except Exception as e:
            log(out, f"  ✘  PORT {port}  ►  Error: {str(e)[:60]}", RED)

    log(out, f"\n{'━'*60}", ACCENT3)
    log(out, f"✔  Banner Grab Complete. {grabbed} banner(s) retrieved from {len(ports)} ports.", GREEN)


# ── 6. SSL/TLS Info (Enhanced) ─────────────────────────────────
def ssl_info(target, out):
    clear(out)
    log_section(out, f"SSL/TLS CERTIFICATE INFO  ►  {target}")
    log(out, "⏳ Retrieving certificate details...\n", YELLOW)

    try:
        # Get certificate with verification
        ctx_verify = ssl.create_default_context()
        try:
            conn_v = ctx_verify.wrap_socket(
                socket.create_connection((target, 443), timeout=10),
                server_hostname=target
            )
            cert = conn_v.getpeercert()
            cipher = conn_v.cipher()
            version = conn_v.version()
            verified = True
            conn_v.close()
        except ssl.SSLCertVerificationError:
            verified = False
            ctx_noverify = ssl.create_default_context()
            ctx_noverify.check_hostname = False
            ctx_noverify.verify_mode = ssl.CERT_NONE
            conn_nv = ctx_noverify.wrap_socket(
                socket.create_connection((target, 443), timeout=10),
                server_hostname=target
            )
            cert = conn_nv.getpeercert()
            cipher = conn_nv.cipher()
            version = conn_nv.version()
            conn_nv.close()

        # Connection Info
        log_subsection(out, "CONNECTION DETAILS")
        log(out, f"  Protocol         ►  {version}", ACCENT)
        log(out, f"  Cipher Suite     ►  {cipher[0]}", ACCENT)
        log(out, f"  Key Bits         ►  {cipher[2]}", TEXT)
        if verified:
            log(out, f"  Verification     ►  ✔ VALID (Trusted CA)", GREEN)
        else:
            log(out, f"  Verification     ►  ⚠ UNTRUSTED / Self-Signed", RED)

        # Subject
        if cert:
            subject = dict(x[0] for x in cert.get("subject", []))
            issuer  = dict(x[0] for x in cert.get("issuer", []))

            log_subsection(out, "CERTIFICATE SUBJECT")
            for k, v in subject.items():
                log(out, f"  {k:<28} ►  {v}", TEXT)

            log_subsection(out, "CERTIFICATE ISSUER")
            for k, v in issuer.items():
                log(out, f"  {k:<28} ►  {v}", TEXT)

            # Validity dates with expiry check
            log_subsection(out, "VALIDITY PERIOD")
            nb = cert.get("notBefore", "N/A")
            na = cert.get("notAfter", "N/A")
            log(out, f"  Valid From       ►  {nb}", GREEN)

            # Check if expired
            try:
                expiry = datetime.strptime(na, "%b %d %H:%M:%S %Y %Z")
                days_left = (expiry - datetime.now()).days
                if days_left > 30:
                    log(out, f"  Expires          ►  {na}  ({days_left} days remaining)", GREEN)
                elif days_left > 0:
                    log(out, f"  Expires          ►  {na}  (⚠ Only {days_left} days remaining!)", ORANGE)
                else:
                    log(out, f"  Expires          ►  {na}  (✘ EXPIRED {abs(days_left)} days ago!)", RED)
            except Exception:
                log(out, f"  Expires          ►  {na}", TEXT)

            # SANs
            san = cert.get("subjectAltName", [])
            if san:
                log_subsection(out, f"SUBJECT ALT NAMES ({len(san)} entries)")
                for kind, val in san:
                    log(out, f"  {kind:<16} ►  {val}", CYAN)

            # Serial Number
            serial = cert.get("serialNumber", "")
            if serial:
                log(out, f"\n  Serial Number    ►  {serial}", TEXT_DIM)

            # OCSP
            ocsp = cert.get("OCSP", [])
            if ocsp:
                for url in ocsp:
                    log(out, f"  OCSP             ►  {url}", TEXT_DIM)

        log(out, f"\n{'━'*60}", ACCENT3)
        log(out, "✔  SSL/TLS Info Complete — Full certificate analysis done.", GREEN)

    except ssl.SSLError as e:
        log(out, f"  ✘  SSL Error: {e}", RED)
    except ConnectionRefusedError:
        log(out, f"  ✘  Port 443 is closed on {target}", RED)
    except socket.timeout:
        log(out, f"  ✘  Connection timed out to {target}:443", RED)
    except Exception as e:
        log(out, f"  ✘  Error: {e}", RED)


# ── 7. IP / GeoLocation Info (Multi-API, merged results) ──────
def geo_info(target, out):
    clear(out)
    log_section(out, f"IP GEO-INTELLIGENCE  ►  {target}")
    log(out, "⏳ Querying multiple IP intelligence sources...\n", YELLOW)

    # Resolve target
    try:
        ip = socket.gethostbyname(target)
        log(out, f"  ✔  Resolved IP  ►  {ip}", ACCENT)
        if ip != target:
            log(out, f"  ✔  Domain       ►  {target}", CYAN)
    except Exception:
        ip = target

    # Validate IP
    try:
        ip_obj = ipaddress.ip_address(ip)
        if ip_obj.is_private:
            log(out, f"  ⚠  This is a PRIVATE IP address — geo lookup may not work.", ORANGE)
        elif ip_obj.is_loopback:
            log(out, f"  ⚠  This is a LOOPBACK address.", ORANGE)
    except Exception:
        pass

    # Multiple API sources for accuracy cross-checking
    merged_data = {}

    # Source 1: ip-api.com (no key needed, good accuracy)
    try:
        url1 = f"http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,asname,query,mobile,proxy,hosting"
        req = urllib.request.Request(url1, headers={"User-Agent": "PhantomRecon/2.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            d1 = json.loads(r.read().decode())
        if d1.get("status") == "success":
            merged_data["source1"] = d1
            log(out, f"  ✔  Source 1 (ip-api.com)  ►  Data received", GREEN2)
    except Exception as e:
        log(out, f"  ℹ  Source 1 (ip-api.com)  ►  {e}", TEXT_DIM)

    # Source 2: ipinfo.io
    try:
        url2 = f"https://ipinfo.io/{ip}/json"
        ctx = ssl.create_default_context()
        req = urllib.request.Request(url2, headers={"User-Agent": "PhantomRecon/2.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
            d2 = json.loads(r.read().decode())
        merged_data["source2"] = d2
        log(out, f"  ✔  Source 2 (ipinfo.io)   ►  Data received", GREEN2)
    except Exception as e:
        log(out, f"  ℹ  Source 2 (ipinfo.io)   ►  {e}", TEXT_DIM)

    if not merged_data:
        log(out, "  ✘  All IP intelligence APIs failed.", RED)
        return

    # Display merged results
    log(out, "", TEXT)

    if "source1" in merged_data:
        d = merged_data["source1"]
        log_subsection(out, "GEOLOCATION DATA")
        log(out, f"  IP Address       ►  {d.get('query', ip)}", ACCENT)
        log(out, f"  Country          ►  {d.get('country', 'N/A')} ({d.get('countryCode', '')})", TEXT)
        log(out, f"  Region           ►  {d.get('regionName', 'N/A')}", TEXT)
        log(out, f"  City             ►  {d.get('city', 'N/A')}", TEXT)
        log(out, f"  ZIP / Postal     ►  {d.get('zip', 'N/A')}", TEXT)
        log(out, f"  Latitude         ►  {d.get('lat', 'N/A')}", CYAN)
        log(out, f"  Longitude        ►  {d.get('lon', 'N/A')}", CYAN)
        log(out, f"  Timezone         ►  {d.get('timezone', 'N/A')}", TEXT)

        log_subsection(out, "NETWORK INTELLIGENCE")
        log(out, f"  ISP              ►  {d.get('isp', 'N/A')}", TEXT)
        log(out, f"  Organization     ►  {d.get('org', 'N/A')}", TEXT)
        log(out, f"  AS Number        ►  {d.get('as', 'N/A')}", TEXT)
        log(out, f"  AS Name          ►  {d.get('asname', 'N/A')}", TEXT)

        # Security flags
        log_subsection(out, "SECURITY FLAGS")
        is_mobile = d.get('mobile', False)
        is_proxy = d.get('proxy', False)
        is_hosting = d.get('hosting', False)
        log(out, f"  Mobile Network   ►  {'Yes ⚠' if is_mobile else 'No'}", ORANGE if is_mobile else GREEN)
        log(out, f"  Proxy / VPN      ►  {'Yes ⚠' if is_proxy else 'No'}", ORANGE if is_proxy else GREEN)
        log(out, f"  Hosting / DC     ►  {'Yes' if is_hosting else 'No'}", CYAN if is_hosting else TEXT)

    elif "source2" in merged_data:
        d = merged_data["source2"]
        log_subsection(out, "GEOLOCATION DATA")
        key_map = {
            "ip": "IP Address", "hostname": "Hostname", "city": "City",
            "region": "Region", "country": "Country",
            "loc": "Coordinates", "org": "Organization / ASN",
            "timezone": "Timezone", "postal": "Postal Code",
        }
        for k, label in key_map.items():
            if k in d and d[k]:
                log(out, f"  {label:<20} ►  {d[k]}", TEXT)

    # Cross-verification
    if "source1" in merged_data and "source2" in merged_data:
        log_subsection(out, "CROSS-VERIFICATION")
        d1 = merged_data["source1"]
        d2 = merged_data["source2"]

        city1 = d1.get("city", "").lower()
        city2 = d2.get("city", "").lower()
        if city1 and city2 and city1 == city2:
            log(out, f"  ✔  City MATCHES across sources: {d1.get('city')}", GREEN)
        elif city1 and city2:
            log(out, f"  ⚠  City DIFFERS: {d1.get('city')} vs {d2.get('city')}", ORANGE)

        country1 = d1.get("countryCode", "").upper()
        country2 = d2.get("country", "").upper()
        if country1 and country2 and country1 == country2:
            log(out, f"  ✔  Country MATCHES: {country1}", GREEN)

    log(out, f"\n{'━'*60}", ACCENT3)
    log(out, "✔  Geo-Intelligence Complete — Multi-source data retrieved.", GREEN)


# ── 8. Subdomain Finder (Extended wordlist) ────────────────────
SUBDOMAINS = [
    "www","mail","ftp","smtp","pop","pop3","ns1","ns2","ns3","vpn",
    "remote","admin","portal","webmail","api","dev","test","staging",
    "blog","shop","store","cdn","media","static","img","images","m",
    "mobile","app","apps","git","svn","jira","confluence","jenkins",
    "docker","cloud","login","secure","cpanel","whm","autodiscover",
    "autoconfig","support","help","docs","status","monitor","beta",
    "demo","old","new","db","database","mysql","sql","redis","mongo",
    "backup","files","download","upload","proxy","gateway","lb",
    "node1","node2","web1","web2","mail2","mx","mx1","mx2",
    "internal","intranet","extranet","ssh","telnet","dns","dns1",
    "dns2","ntp","sip","voip","pbx","exchange","owa","calendar",
    "wiki","forum","boards","chat","irc","slack","teams",
    "grafana","kibana","elastic","es","kafka","rabbitmq","mq",
    "s3","storage","assets","video","stream","live","edge",
    "staging2","uat","qa","prod","production","stg",
]

def subdomain_enum(domain, out):
    clear(out)
    log_section(out, f"SUBDOMAIN ENUMERATION  ►  {domain}")
    log(out, f"⏳ Testing {len(SUBDOMAINS)} subdomain prefixes...\n", YELLOW)

    found = []
    not_found = 0
    for i, sub in enumerate(SUBDOMAINS):
        if is_stopped():
            log(out, "\n  ⛔  Enumeration stopped by user.", ORANGE)
            break
        fqdn = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(fqdn)
            found.append((fqdn, ip))
            log(out, f"  ✔  {fqdn:<45} ►  {ip}", GREEN)
        except socket.gaierror:
            not_found += 1
        except Exception:
            not_found += 1

    log(out, "", TEXT)
    log_subsection(out, "ENUMERATION SUMMARY")
    log(out, f"  ✔  Found             ►  {len(found)} subdomains", GREEN if found else YELLOW)
    log(out, f"  ✘  Not Found         ►  {not_found}", TEXT_DIM)
    log(out, f"  ℹ  Total Tested      ►  {len(SUBDOMAINS)}", TEXT)

    if found:
        log(out, "", TEXT)
        log(out, "  ┌─────────────────────────────────────────────────────────┐", ACCENT3)
        log(out, "  │  SUBDOMAIN                              IP ADDRESS     │", ACCENT)
        log(out, "  ├─────────────────────────────────────────────────────────┤", ACCENT3)
        for fqdn, ip in found:
            log(out, f"  │  {fqdn:<40} {ip:<17}│", GREEN2)
        log(out, "  └─────────────────────────────────────────────────────────┘", ACCENT3)

    log(out, f"\n{'━'*60}", ACCENT3)
    log(out, f"✔  Subdomain Enumeration Complete. {len(found)} discovered.", GREEN if found else YELLOW)


# ── 9. Network Info (Enhanced) ─────────────────────────────────
def network_info(out):
    clear(out)
    log_section(out, "LOCAL NETWORK INTELLIGENCE")
    log(out, "⏳ Gathering comprehensive network details...\n", YELLOW)

    # Hostname & local IPs
    log_subsection(out, "HOST INFORMATION")
    try:
        h = socket.gethostname()
        log(out, f"  Hostname          ►  {h}", TEXT)
        ips = socket.getaddrinfo(h, None)
        seen = set()
        for r in ips:
            addr = r[4][0]
            if addr not in seen:
                seen.add(addr)
                addr_type = "IPv4" if r[0] == socket.AF_INET else "IPv6"
                log(out, f"  Local {addr_type:<5}      ►  {addr}", GREEN)
    except Exception as e:
        log(out, f"  ✘  Hostname error: {e}", RED)

    # Platform info
    log_subsection(out, "SYSTEM INFORMATION")
    log(out, f"  OS               ►  {platform.system()} {platform.release()}", TEXT)
    log(out, f"  OS Version       ►  {platform.version()}", TEXT)
    log(out, f"  Architecture     ►  {platform.machine()}", TEXT)
    log(out, f"  Processor        ►  {platform.processor()[:60]}", TEXT)
    log(out, f"  Python Version   ►  {platform.python_version()}", TEXT)
    log(out, f"  Node Name        ►  {platform.node()}", TEXT)

    # Network interfaces
    log_subsection(out, "NETWORK INTERFACES")
    try:
        if platform.system() == "Windows":
            cmd = ["ipconfig", "/all"]
        else:
            cmd = ["ip", "addr"] if os.path.exists("/bin/ip") else ["ifconfig", "-a"]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=8,
                                creationflags=0x08000000 if platform.system() == "Windows" else 0)

        important_keys = [
            "ipv4", "ipv6", "inet", "subnet", "mask", "gateway",
            "mac", "physical", "ether", "adapter", "dns server",
            "dhcp", "lease", "description", "connection-specific"
        ]

        for line in result.stdout.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            # Section headers (adapter names)
            if not line.startswith(" ") and ":" in stripped:
                log(out, f"\n  ── {stripped} ──", YELLOW)
            elif any(k in stripped.lower() for k in important_keys):
                log(out, f"    {stripped}", TEXT)
    except Exception as e:
        log(out, f"  ✘  Error: {e}", RED)

    # Public IP with details
    log_subsection(out, "PUBLIC IP & EXTERNAL DETAILS")
    try:
        ctx = ssl.create_default_context()
        req = urllib.request.Request("https://api.ipify.org?format=json",
                                     headers={"User-Agent": "PhantomRecon/2.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=8) as r:
            data = json.loads(r.read())
            pub_ip = data['ip']
            log(out, f"  Public IP        ►  {pub_ip}", ACCENT)

            # Get details about public IP
            try:
                req2 = urllib.request.Request(f"http://ip-api.com/json/{pub_ip}",
                                              headers={"User-Agent": "PhantomRecon/2.0"})
                with urllib.request.urlopen(req2, timeout=8) as r2:
                    geo = json.loads(r2.read())
                    log(out, f"  ISP              ►  {geo.get('isp', 'N/A')}", TEXT)
                    log(out, f"  Organization     ►  {geo.get('org', 'N/A')}", TEXT)
                    log(out, f"  Location         ►  {geo.get('city', '')}, {geo.get('country', '')}", TEXT)
                    log(out, f"  AS               ►  {geo.get('as', 'N/A')}", TEXT)
            except Exception:
                pass
    except Exception:
        log(out, "  ℹ  Could not fetch public IP (no internet?)", TEXT_DIM)

    # Default gateway via routing table
    log_subsection(out, "ROUTING TABLE (Summary)")
    try:
        if platform.system() == "Windows":
            result = subprocess.run(["route", "print", "0.0.0.0"], capture_output=True, text=True, timeout=5,
                                    creationflags=0x08000000 if platform.system() == "Windows" else 0)
        else:
            result = subprocess.run(["ip", "route", "show", "default"], capture_output=True, text=True, timeout=5)

        for line in result.stdout.splitlines():
            stripped = line.strip()
            if stripped and any(k in stripped.lower() for k in ["0.0.0.0", "default", "gateway"]):
                log(out, f"    {stripped}", TEXT)
    except Exception:
        pass

    log(out, f"\n{'━'*60}", ACCENT3)
    log(out, "✔  Network Intelligence Complete.", GREEN)


# ═══════════════════════ SPLASH SCREEN ═════════════════════════
class SplashScreen:
    def __init__(self, parent):
        self.parent = parent
        self.splash = tk.Toplevel(parent)
        self.splash.overrideredirect(True)
        self.splash.configure(bg="#000000")
        self.splash.attributes("-alpha", 0.0)

        # Center on screen
        w, h = 600, 400
        sw = self.splash.winfo_screenwidth()
        sh = self.splash.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.splash.geometry(f"{w}x{h}+{x}+{y}")

        # Background
        canvas = tk.Canvas(self.splash, width=w, height=h, bg="#050812",
                          highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)

        # Decorative lines
        for i in range(0, w, 30):
            alpha_color = f"#{max(5, 10 - abs(i - w//2)//30):02x}{max(10, 20 - abs(i - w//2)//30):02x}{max(30, 50 - abs(i - w//2)//20):02x}"
            canvas.create_line(i, 0, i, h, fill=alpha_color, width=1)

        # Main title
        canvas.create_text(w//2, 100, text="⚡", font=("Segoe UI", 50), fill=ACCENT)
        canvas.create_text(w//2, 170, text="PHANTOM RECON", font=("Consolas", 32, "bold"), fill=ACCENT)
        canvas.create_text(w//2, 210, text="S U I T E   v 2 . 0", font=("Consolas", 16), fill=CYAN)
        canvas.create_text(w//2, 260, text="Footprinting & Reconnaissance Toolkit",
                          font=("Segoe UI", 13), fill=TEXT_DIM)
        canvas.create_text(w//2, 290, text="CEH / eJPT Study & Ethical Pen Testing",
                          font=("Segoe UI", 11), fill=TEXT_DIM)

        # Loading bar background
        canvas.create_rectangle(100, 340, 500, 348, fill="#0a1020", outline="#1a2744")
        self.loading_bar = canvas.create_rectangle(100, 340, 100, 348, fill=ACCENT, outline="")
        self.canvas = canvas
        self.bar_width = 400

        # Version info
        canvas.create_text(w//2, 375, text="Built with Python 3 — No Dependencies Required",
                          font=("Segoe UI", 9), fill="#3a4a6b")

        # Animate
        self.progress = 0
        self._fade_in()

    def _fade_in(self):
        alpha = self.splash.attributes("-alpha")
        if alpha < 1.0:
            self.splash.attributes("-alpha", min(1.0, alpha + 0.08))
            self.splash.after(20, self._fade_in)
        else:
            self._animate_bar()

    def _animate_bar(self):
        if self.progress < self.bar_width:
            self.progress += 8
            self.canvas.coords(self.loading_bar, 100, 340, 100 + self.progress, 348)

            # Change color as it progresses
            pct = self.progress / self.bar_width
            if pct > 0.7:
                self.canvas.itemconfigure(self.loading_bar, fill=GREEN)
            elif pct > 0.4:
                self.canvas.itemconfigure(self.loading_bar, fill=CYAN)

            self.splash.after(15, self._animate_bar)
        else:
            self.splash.after(400, self._fade_out)

    def _fade_out(self):
        alpha = self.splash.attributes("-alpha")
        if alpha > 0.0:
            self.splash.attributes("-alpha", max(0.0, alpha - 0.1))
            self.splash.after(20, self._fade_out)
        else:
            self.splash.destroy()
            self.parent.deiconify()


# ═══════════════════════ MAIN GUI CLASS ════════════════════════
class PhantomReconSuite:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("⚡ PHANTOM RECON SUITE v2.0  —  Ethical Hacking & Reconnaissance Toolkit")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 750)
        self.root.configure(bg=BG)
        self.root.resizable(True, True)

        # Hide main window, show splash
        self.root.withdraw()

        # Store all results for report
        self.scan_log = []
        self.pulse_state = True

        self._styles()
        self._header()
        self._notebook()
        self._footer()

        # Show splash screen
        SplashScreen(self.root)

        # Start status pulse animation
        self._pulse_status()

        self.root.mainloop()

    # ── Styles ─────────────────────────────────────────────────
    def _styles(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("TNotebook", background=BG, borderwidth=0, tabmargins=[2, 2, 2, 0])
        s.configure("TNotebook.Tab",
                    background=PANEL, foreground=TEXT_DIM,
                    padding=[12, 8], font=TAB_FONT,
                    borderwidth=0, focuscolor=BG)
        s.map("TNotebook.Tab",
              background=[("selected", BG2)],
              foreground=[("selected", ACCENT)])
        s.configure("TFrame", background=BG)

    # ── Header ─────────────────────────────────────────────────
    def _header(self):
        # Top bar with gradient effect
        hdr = tk.Frame(self.root, bg=BG2, pady=0)
        hdr.pack(fill=tk.X)

        left = tk.Frame(hdr, bg=BG2)
        left.pack(side=tk.LEFT, padx=24, pady=14)

        tk.Label(left, text="⚡ PHANTOM RECON SUITE",
                 font=TITLE_FONT, bg=BG2, fg=ACCENT).pack(side=tk.LEFT)
        tk.Label(left, text="  v2.0  │  Footprinting & Reconnaissance Toolkit  │  CEH / eJPT Study",
                 font=SUB_FONT, bg=BG2, fg=TEXT_DIM).pack(side=tk.LEFT, pady=2)

        right = tk.Frame(hdr, bg=BG2)
        right.pack(side=tk.RIGHT, padx=24)

        # Clock
        self.clock_var = tk.StringVar(value=datetime.now().strftime("%H:%M:%S"))
        tk.Label(right, textvariable=self.clock_var,
                 font=("Consolas", 12), bg=BG2, fg=TEXT_DIM).pack(side=tk.RIGHT, padx=(12, 0))

        self.status_var = tk.StringVar(value="● READY")
        self.status_label = tk.Label(right, textvariable=self.status_var,
                 font=STATUS_FONT, bg=BG2, fg=GREEN)
        self.status_label.pack(side=tk.RIGHT)

        # Update clock
        self._update_clock()

        # Accent line with glow
        tk.Frame(self.root, bg=ACCENT, height=2).pack(fill=tk.X)
        tk.Frame(self.root, bg=GLOW, height=1).pack(fill=tk.X)

    def _update_clock(self):
        self.clock_var.set(datetime.now().strftime("%H:%M:%S"))
        self.root.after(1000, self._update_clock)

    def _pulse_status(self):
        """Pulsing status indicator animation"""
        if self.pulse_state:
            self.status_label.configure(fg=GREEN)
        else:
            self.status_label.configure(fg=GREEN2)
        self.pulse_state = not self.pulse_state
        self.root.after(800, self._pulse_status)

    # ── Notebook ───────────────────────────────────────────────
    def _notebook(self):
        self.nb = ttk.Notebook(self.root)
        self.nb.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        self._tab_dns()
        self._tab_whois()
        self._tab_portscan()
        self._tab_traceroute()
        self._tab_banner()
        self._tab_ssl()
        self._tab_geo()
        self._tab_subdomain()
        self._tab_netinfo()
        self._tab_report()

    # ── Footer ─────────────────────────────────────────────────
    def _footer(self):
        ft = tk.Frame(self.root, bg="#040610", pady=6)
        ft.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(ft,
                 text="⚠  FOR EDUCATIONAL & AUTHORIZED TESTING ONLY  │  "
                      "Unauthorized scanning is ILLEGAL  │  "
                      "Phantom Recon Suite v2.0 — Waqar's CEH Toolkit",
                 font=FOOTER_FONT, bg="#040610", fg=TEXT_DIM).pack()

    # ══════════════════════ TABS ════════════════════════════════

    # ─── DNS ───────────────────────────────────────────────────
    def _tab_dns(self):
        f = ttk.Frame(self.nb)
        self.nb.add(f, text=" DNS ")

        ctrl = tk.Frame(f, bg=BG, pady=8)
        ctrl.pack(fill=tk.X)

        self.dns_entry = make_entry(ctrl, "Target Domain:", 50)
        self.dns_entry.insert(0, "example.com")

        btn_row = tk.Frame(f, bg=BG)
        btn_row.pack(fill=tk.X, padx=14)
        self.dns_out = make_output(f)

        run_cmd = lambda: thread(dns_lookup, self.dns_entry.get().strip(), self.dns_out)
        fancy_button(btn_row, "▶  Run DNS Lookup", run_cmd)
        fancy_button(btn_row, "⏹  Stop", stop_scan, RED, True)
        fancy_button(btn_row, "⬛  Clear",
                     lambda: clear(self.dns_out), TEXT_DIM, False)
        self.dns_entry.bind("<Return>", lambda e: run_cmd())

        self._info_label(f, "Enumerates A, AAAA, MX, NS, CNAME, TXT, SOA records with cross-verification via reverse DNS.")

    # ─── WHOIS ─────────────────────────────────────────────────
    def _tab_whois(self):
        f = ttk.Frame(self.nb)
        self.nb.add(f, text=" WHOIS ")

        ctrl = tk.Frame(f, bg=BG, pady=8)
        ctrl.pack(fill=tk.X)

        self.whois_entry = make_entry(ctrl, "Domain / IP:", 50)
        self.whois_entry.insert(0, "google.com")

        btn_row = tk.Frame(f, bg=BG)
        btn_row.pack(fill=tk.X, padx=14)
        self.whois_out = make_output(f)

        run_cmd = lambda: thread(whois_lookup, self.whois_entry.get().strip(), self.whois_out)
        fancy_button(btn_row, "▶  Run WHOIS", run_cmd)
        fancy_button(btn_row, "⏹  Stop", stop_scan, RED, True)
        fancy_button(btn_row, "⬛  Clear", lambda: clear(self.whois_out), TEXT_DIM, False)
        self.whois_entry.bind("<Return>", lambda e: run_cmd())

        self._info_label(f, "RDAP-based WHOIS with multiple fallback sources. Shows registrar, dates, nameservers, contacts.")

    # ─── PORT SCAN ─────────────────────────────────────────────
    def _tab_portscan(self):
        f = ttk.Frame(self.nb)
        self.nb.add(f, text=" Ports ")

        ctrl = tk.Frame(f, bg=BG, pady=8)
        ctrl.pack(fill=tk.X)

        self.ps_entry = make_entry(ctrl, "Target Host:", 40)
        self.ps_entry.insert(0, "scanme.nmap.org")
        self.ps_range = make_entry(ctrl, "Ports (top / 1-1024 / 80,443):", 25)
        self.ps_range.insert(0, "top")

        btn_row = tk.Frame(f, bg=BG)
        btn_row.pack(fill=tk.X, padx=14)
        self.ps_out = make_output(f)

        run_cmd = lambda: thread(port_scan,
                                 self.ps_entry.get().strip(),
                                 self.ps_range.get().strip(),
                                 self.ps_out)
        fancy_button(btn_row, "▶  Start Scan", run_cmd)
        fancy_button(btn_row, "⏹  Stop", stop_scan, RED, True)
        fancy_button(btn_row, "⬛  Clear", lambda: clear(self.ps_out), TEXT_DIM, False)
        self.ps_entry.bind("<Return>", lambda e: run_cmd())
        self.ps_range.bind("<Return>", lambda e: run_cmd())

        self._info_label(f, f"TCP Connect scan with inline banner grab. 'top' scans {len(COMMON_PORTS)} well-known ports. Results include summary table.")

    # ─── TRACEROUTE ────────────────────────────────────────────
    def _tab_traceroute(self):
        f = ttk.Frame(self.nb)
        self.nb.add(f, text=" Trace ")

        ctrl = tk.Frame(f, bg=BG, pady=8)
        ctrl.pack(fill=tk.X)

        self.tr_entry = make_entry(ctrl, "Target Host:", 50)
        self.tr_entry.insert(0, "google.com")

        btn_row = tk.Frame(f, bg=BG)
        btn_row.pack(fill=tk.X, padx=14)
        self.tr_out = make_output(f)

        run_cmd = lambda: thread(traceroute, self.tr_entry.get().strip(), self.tr_out)
        fancy_button(btn_row, "▶  Trace Route", run_cmd)
        fancy_button(btn_row, "⏹  Stop", stop_scan, RED, True)
        fancy_button(btn_row, "⬛  Clear", lambda: clear(self.tr_out), TEXT_DIM, False)
        self.tr_entry.bind("<Return>", lambda e: run_cmd())

        self._info_label(f, "Traces network hops with color-coded latency. Uses tracert (Windows) or traceroute (Linux/Mac).")

    # ─── BANNER GRABBER ────────────────────────────────────────
    def _tab_banner(self):
        f = ttk.Frame(self.nb)
        self.nb.add(f, text=" Banner ")

        ctrl = tk.Frame(f, bg=BG, pady=8)
        ctrl.pack(fill=tk.X)

        self.bg_entry = make_entry(ctrl, "Target Host:", 40)
        self.bg_entry.insert(0, "scanme.nmap.org")
        self.bg_ports = make_entry(ctrl, "Ports (comma sep):", 30)
        self.bg_ports.insert(0, "21,22,25,80,443,8080")

        btn_row = tk.Frame(f, bg=BG)
        btn_row.pack(fill=tk.X, padx=14)
        self.bg_out = make_output(f)

        run_cmd = lambda: thread(banner_grab,
                                 self.bg_entry.get().strip(),
                                 self.bg_ports.get().strip(),
                                 self.bg_out)
        fancy_button(btn_row, "▶  Grab Banners", run_cmd)
        fancy_button(btn_row, "⏹  Stop", stop_scan, RED, True)
        fancy_button(btn_row, "⬛  Clear", lambda: clear(self.bg_out), TEXT_DIM, False)
        self.bg_entry.bind("<Return>", lambda e: run_cmd())
        self.bg_ports.bind("<Return>", lambda e: run_cmd())

        self._info_label(f, "Protocol-aware banner grabbing with SSL support. Identifies server software, versions, and headers.")

    # ─── SSL ───────────────────────────────────────────────────
    def _tab_ssl(self):
        f = ttk.Frame(self.nb)
        self.nb.add(f, text=" SSL ")

        ctrl = tk.Frame(f, bg=BG, pady=8)
        ctrl.pack(fill=tk.X)

        self.ssl_entry = make_entry(ctrl, "Domain (HTTPS):", 50)
        self.ssl_entry.insert(0, "google.com")

        btn_row = tk.Frame(f, bg=BG)
        btn_row.pack(fill=tk.X, padx=14)
        self.ssl_out = make_output(f)

        run_cmd = lambda: thread(ssl_info, self.ssl_entry.get().strip(), self.ssl_out)
        fancy_button(btn_row, "▶  Check SSL", run_cmd)
        fancy_button(btn_row, "⏹  Stop", stop_scan, RED, True)
        fancy_button(btn_row, "⬛  Clear", lambda: clear(self.ssl_out), TEXT_DIM, False)
        self.ssl_entry.bind("<Return>", lambda e: run_cmd())

        self._info_label(f, "Full certificate analysis: subject, issuer, expiry check, SANs, cipher suite, verification status.")

    # ─── GEO INFO ──────────────────────────────────────────────
    def _tab_geo(self):
        f = ttk.Frame(self.nb)
        self.nb.add(f, text=" GeoIP ")

        ctrl = tk.Frame(f, bg=BG, pady=8)
        ctrl.pack(fill=tk.X)

        self.geo_entry = make_entry(ctrl, "IP / Domain:", 50)
        self.geo_entry.insert(0, "8.8.8.8")

        btn_row = tk.Frame(f, bg=BG)
        btn_row.pack(fill=tk.X, padx=14)
        self.geo_out = make_output(f)

        run_cmd = lambda: thread(geo_info, self.geo_entry.get().strip(), self.geo_out)
        fancy_button(btn_row, "▶  Get Geo Info", run_cmd)
        fancy_button(btn_row, "⏹  Stop", stop_scan, RED, True)
        fancy_button(btn_row, "⬛  Clear", lambda: clear(self.geo_out), TEXT_DIM, False)
        self.geo_entry.bind("<Return>", lambda e: run_cmd())

        self._info_label(f, "Multi-source geo-intelligence with cross-verification. Checks ISP, ASN, proxy/VPN, hosting flags.")

    # ─── SUBDOMAIN ─────────────────────────────────────────────
    def _tab_subdomain(self):
        f = ttk.Frame(self.nb)
        self.nb.add(f, text=" Subs ")

        ctrl = tk.Frame(f, bg=BG, pady=8)
        ctrl.pack(fill=tk.X)

        self.sd_entry = make_entry(ctrl, "Base Domain:", 50)
        self.sd_entry.insert(0, "example.com")

        btn_row = tk.Frame(f, bg=BG)
        btn_row.pack(fill=tk.X, padx=14)
        self.sd_out = make_output(f)

        run_cmd = lambda: thread(subdomain_enum, self.sd_entry.get().strip(), self.sd_out)
        fancy_button(btn_row, "▶  Enumerate Subdomains", run_cmd)
        fancy_button(btn_row, "⏹  Stop", stop_scan, RED, True)
        fancy_button(btn_row, "⬛  Clear", lambda: clear(self.sd_out), TEXT_DIM, False)
        self.sd_entry.bind("<Return>", lambda e: run_cmd())

        self._info_label(f, f"DNS brute-force with {len(SUBDOMAINS)} common prefixes. Results displayed in summary table.")

    # ─── NETWORK INFO ──────────────────────────────────────────
    def _tab_netinfo(self):
        f = ttk.Frame(self.nb)
        self.nb.add(f, text=" NetInfo ")

        btn_row = tk.Frame(f, bg=BG, pady=12)
        btn_row.pack(fill=tk.X, padx=14)
        self.ni_out = make_output(f, height=22)

        run_cmd = lambda: thread(network_info, self.ni_out)
        fancy_button(btn_row, "▶  Get Network Info", run_cmd)
        fancy_button(btn_row, "⏹  Stop", stop_scan, RED, True)
        fancy_button(btn_row, "⬛  Clear", lambda: clear(self.ni_out), TEXT_DIM, False)

        self._info_label(f, "Comprehensive local network intelligence: hostname, IPs, interfaces, public IP with ISP details, routing.")

    # ─── REPORT ────────────────────────────────────────────────
    def _tab_report(self):
        f = ttk.Frame(self.nb)
        self.nb.add(f, text=" Report ")

        # Description
        desc_frame = tk.Frame(f, bg=BG, pady=8)
        desc_frame.pack(fill=tk.X, padx=14)
        tk.Label(desc_frame,
                 text="Export all scan results to a professional PDF report",
                 bg=BG, fg=CYAN, font=UI).pack(anchor="w")

        self.report_target = make_entry(f, "Target (label):", 40)
        self.report_target.insert(0, "example.com")

        btn_row = tk.Frame(f, bg=BG, pady=8)
        btn_row.pack(fill=tk.X, padx=14)

        fancy_button(btn_row, "Export PDF Report", self._export_report)
        fancy_button(btn_row, "Copy All Results", self._copy_all, ACCENT2)

        self.rep_out = make_output(f, height=18)
        log(self.rep_out, "----------------------------------------------------", ACCENT3)
        log(self.rep_out, "  Run scans in any tab, then click 'Export PDF Report'.", ACCENT)
        log(self.rep_out, "  Reports are saved as professional PDF files.", TEXT_DIM)
        log(self.rep_out, "  Use 'Copy All Results' to paste into documents.", TEXT_DIM)
        log(self.rep_out, "----------------------------------------------------", ACCENT3)

    def _export_report(self):
        target = self.report_target.get().strip() or "recon"
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile=f"phantom_recon_{target}_{ts}.pdf",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        if not filename:
            return

        content = self._collect_all_outputs()
        if not content.strip():
            messagebox.showwarning("No Data", "Run scans first before exporting.")
            return

        try:
            self._generate_pdf(filename, target, content)
            log(self.rep_out, f"\n[OK]  PDF Report saved: {filename}", GREEN)
            messagebox.showinfo("Report Saved", f"PDF Report exported to:\n{filename}")
        except Exception as e:
            log(self.rep_out, f"\n[ERROR]  PDF export failed: {e}", RED)
            messagebox.showerror("Export Error", f"Failed to create PDF:\n{e}")

    def _generate_pdf(self, filepath, target, content):
        """Generate a proper PDF report using raw PDF format (no dependencies)."""
        def clean_text(s):
            replacements = {
                '\u2500': '-', '\u2501': '=', '\u2502': '|', '\u2503': '|',
                '\u250c': '+', '\u250d': '+', '\u2510': '+', '\u2514': '+',
                '\u2518': '+', '\u251c': '+', '\u2524': '+', '\u252c': '+',
                '\u2534': '+', '\u253c': '+', '\u2550': '=', '\u2551': '|',
                '\u2554': '+', '\u2557': '+', '\u255a': '+', '\u255d': '+',
                '\u2560': '+', '\u2563': '+', '\u2566': '+', '\u2569': '+',
                '\u256c': '+', '\u2588': '#', '\u2591': '.', '\u2592': ':',
                '\u2593': '#', '\u25a0': '#', '\u25cf': '*', '\u25c6': '*',
                '\u2716': 'x', '\u2714': '+', '\u2718': 'x', '\u2713': '+',
                '\u2605': '*', '\u2606': '*', '\u26a0': '!', '\u26a1': '>',
                '\u2022': '*', '\u25ba': '>', '\u25b6': '>', '\u2192': '->',
                '\u2190': '<-', '\u2191': '^', '\u2193': 'v',
                '\u2584': '_', '\u2580': '-',
                '\u231b': '[TIME]', '\u2328': '[KEY]',
                '\u2709': '[MAIL]', '\u260e': '[TEL]',
                '\u2139': '[i]', '\u24d8': '[i]',
                '\u25ac': '-',
                '\u2523': '+', '\u252b': '+', '\u2533': '+', '\u253b': '+',
                '\u254b': '+',
                '\u250f': '+', '\u2513': '+', '\u2517': '+', '\u251b': '+',
                '\u2578': '-', '\u257a': '-', '\u2579': '|', '\u257b': '|',
                '\u2574': '-', '\u2575': '|', '\u2576': '-', '\u2577': '|',
                '\u2015': '--', '\u2014': '--', '\u2013': '-',
                '\u2026': '...', '\u25cb': 'o',
                '\u25b2': '^', '\u25bc': 'v',
                '\u00bb': '>>', '\u00ab': '<<',
                '\u258c': '|', '\u2590': '|',
                '\u2023': '>', '\u2043': '-', '\ufffd': '?',
                '\u2610': '[ ]', '\u2611': '[x]', '\u2612': '[X]',
            }
            result = []
            for ch in s:
                if ch in replacements:
                    result.append(replacements[ch])
                elif ord(ch) < 256:
                    result.append(ch)
                else:
                    result.append('?')
            return ''.join(result)

        def pdf_escape(s):
            s = clean_text(s)
            s = s.replace('\\', '\\\\')
            s = s.replace('(', '\\(')
            s = s.replace(')', '\\)')
            return s

        # Page dimensions (A4)
        page_w, page_h = 595, 842
        margin_left = 40
        margin_top, margin_bottom = 50, 40
        font_size = 9
        title_size = 18
        subtitle_size = 11
        line_height = font_size + 3
        max_chars = 95

        # Prepare all lines
        header_lines = [
            f"Target : {target}",
            f"Date   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"System : {platform.system()} {platform.release()}",
            "=" * 65,
        ]
        body_lines = content.splitlines()
        all_lines = header_lines + [""] + body_lines

        # Word-wrap
        wrapped = []
        for line in all_lines:
            line = line.rstrip()
            if len(line) <= max_chars:
                wrapped.append(line)
            else:
                while len(line) > max_chars:
                    brk = line.rfind(' ', 0, max_chars)
                    if brk <= 0:
                        brk = max_chars
                    wrapped.append(line[:brk])
                    line = '    ' + line[brk:].lstrip()
                if line.strip():
                    wrapped.append(line)

        # Split into pages
        title_block_lines = 6
        first_page_max = int((page_h - margin_top - margin_bottom) / line_height) - title_block_lines - 2
        other_page_max = int((page_h - margin_top - margin_bottom) / line_height) - 4

        pages = []
        if len(wrapped) <= first_page_max:
            pages.append(wrapped)
        else:
            pages.append(wrapped[:first_page_max])
            remaining = wrapped[first_page_max:]
            while remaining:
                pages.append(remaining[:other_page_max])
                remaining = remaining[other_page_max:]

        if not pages:
            pages = [["No scan data to report."]]

        # PDF object management
        obj_id = 0
        offsets = {}
        pdf_parts = []

        def new_obj():
            nonlocal obj_id
            obj_id += 1
            return obj_id

        pdf_parts.append(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")

        def write_obj(oid, data):
            offset = sum(len(p) for p in pdf_parts)
            offsets[oid] = offset
            obj_bytes = f"{oid} 0 obj\n{data}\nendobj\n".encode('latin-1', errors='replace')
            pdf_parts.append(obj_bytes)

        cat_id = new_obj()
        pages_id = new_obj()
        font_id = new_obj()
        font_bold_id = new_obj()
        page_obj_ids = [new_obj() for _ in pages]
        content_obj_ids = [new_obj() for _ in pages]

        write_obj(cat_id, f"<< /Type /Catalog /Pages {pages_id} 0 R >>")
        kids = " ".join(f"{pid} 0 R" for pid in page_obj_ids)
        write_obj(pages_id, f"<< /Type /Pages /Kids [{kids}] /Count {len(pages)} >>")
        write_obj(font_id, "<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>")
        write_obj(font_bold_id, "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")

        for i, page_lines in enumerate(pages):
            stream_parts = []
            stream_parts.append("BT")
            y = page_h - margin_top

            if i == 0:
                # Title
                stream_parts.append(f"/F2 {title_size} Tf")
                stream_parts.append(f"1 0 0 1 {margin_left} {y} Tm")
                stream_parts.append(f"({pdf_escape('PHANTOM RECON SUITE v2.0')}) Tj")
                y -= title_size + 8
                stream_parts.append(f"/F2 {subtitle_size} Tf")
                stream_parts.append(f"1 0 0 1 {margin_left} {y} Tm")
                stream_parts.append(f"({pdf_escape('Reconnaissance & Footprinting Report')}) Tj")
                y -= subtitle_size + 14
            else:
                stream_parts.append(f"/F2 {font_size} Tf")
                stream_parts.append(f"1 0 0 1 {margin_left} {y} Tm")
                pg_hdr = f"Phantom Recon Suite v2.0  --  Page {i+1} of {len(pages)}"
                stream_parts.append(f"({pdf_escape(pg_hdr)}) Tj")
                y -= line_height
                stream_parts.append(f"/F1 {font_size} Tf")
                stream_parts.append(f"1 0 0 1 {margin_left} {y} Tm")
                stream_parts.append(f"({pdf_escape('-' * 85)}) Tj")
                y -= line_height + 4

            stream_parts.append(f"/F1 {font_size} Tf")
            for line in page_lines:
                if y < margin_bottom + 20:
                    break
                stream_parts.append(f"1 0 0 1 {margin_left} {y} Tm")
                stripped = clean_text(line).strip()
                is_hdr = (stripped.startswith('===') or
                         stripped.startswith('---') or
                         (len(stripped) > 5 and all(c in '=-+#*' for c in stripped)))
                if is_hdr:
                    stream_parts.append(f"/F2 {font_size} Tf")
                    stream_parts.append(f"({pdf_escape(line)}) Tj")
                    stream_parts.append(f"/F1 {font_size} Tf")
                else:
                    stream_parts.append(f"({pdf_escape(line)}) Tj")
                y -= line_height

            footer_date = datetime.now().strftime('%Y-%m-%d %H:%M')
            footer_txt = f"Phantom Recon Suite v2.0  |  Page {i+1} of {len(pages)}  |  Generated {footer_date}"
            stream_parts.append(f"/F1 7 Tf")
            stream_parts.append(f"1 0 0 1 {margin_left} 22 Tm")
            stream_parts.append(f"({pdf_escape(footer_txt)}) Tj")
            stream_parts.append("ET")

            stream_data = "\n".join(stream_parts)
            write_obj(content_obj_ids[i],
                     f"<< /Length {len(stream_data)} >>\nstream\n{stream_data}\nendstream")
            write_obj(page_obj_ids[i],
                     f"<< /Type /Page /Parent {pages_id} 0 R "
                     f"/MediaBox [0 0 {page_w} {page_h}] "
                     f"/Contents {content_obj_ids[i]} 0 R "
                     f"/Resources << /Font << /F1 {font_id} 0 R /F2 {font_bold_id} 0 R >> >> >>")

        xref_offset = sum(len(p) for p in pdf_parts)
        xref_lines = ["xref", f"0 {obj_id + 1}", "0000000000 65535 f "]
        for oid in range(1, obj_id + 1):
            xref_lines.append(f"{offsets[oid]:010d} 00000 n ")
        xref_lines.append("")
        trailer = (
            f"trailer\n<< /Size {obj_id + 1} /Root {cat_id} 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF\n"
        )
        pdf_parts.append("\n".join(xref_lines).encode('latin-1'))
        pdf_parts.append(trailer.encode('latin-1'))

        with open(filepath, 'wb') as f:
            for part in pdf_parts:
                f.write(part)

    def _copy_all(self):
        content = self._collect_all_outputs()
        if not content.strip():
            messagebox.showwarning("⚠ No Data", "Run scans first before copying results.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        log(self.rep_out, "✔  All results copied to clipboard.", GREEN)

    def _collect_all_outputs(self):
        outputs = {
            "DNS Lookup":   getattr(self, "dns_out",    None),
            "WHOIS":        getattr(self, "whois_out",  None),
            "Port Scanner": getattr(self, "ps_out",     None),
            "Traceroute":   getattr(self, "tr_out",     None),
            "Banner Grab":  getattr(self, "bg_out",     None),
            "SSL/TLS":      getattr(self, "ssl_out",    None),
            "Geo Intel":    getattr(self, "geo_out",    None),
            "Subdomains":   getattr(self, "sd_out",     None),
            "Network Info": getattr(self, "ni_out",     None),
        }
        lines = []
        for name, widget in outputs.items():
            if widget:
                widget.config(state=tk.NORMAL)
                text = widget.get(1.0, tk.END).strip()
                widget.config(state=tk.DISABLED)
                if text:
                    lines.append(f"\n{'═'*60}\n  {name}\n{'═'*60}\n{text}\n")
        return "\n".join(lines)

    # ─── Shared helper ─────────────────────────────────────────
    def _info_label(self, parent, text):
        info_frame = tk.Frame(parent, bg=BG)
        info_frame.pack(fill=tk.X, padx=14, pady=(0, 6))
        tk.Label(info_frame, text=f"ℹ  {text}",
                 bg=BG, fg=TEXT_DIM,
                 font=INFO_FONT,
                 anchor="w", wraplength=1100,
                 justify=tk.LEFT).pack(fill=tk.X)


# ═══════════════════════ ENTRY POINT ═══════════════════════════
if __name__ == "__main__":
    import sys
    import io
    # Fix console encoding for Unicode on Windows
    if sys.platform == "win32":
        try:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        except Exception:
            pass
    try:
        print("""
+======================================================+
|       PHANTOM RECON SUITE v2.0 launching...          |
|       Footprinting & Reconnaissance Toolkit          |
|       For Ethical Hacking & CEH Preparation          |
|       Enhanced UI + Accurate Multi-Source Intel       |
+======================================================+
        """)
    except Exception:
        print("Phantom Recon Suite v2.0 launching...")
    PhantomReconSuite()