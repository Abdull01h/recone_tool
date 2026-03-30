import socket
import requests
from bs4 import BeautifulSoup
import re
import os
import time
import whois

# --- CONFIGURATION ---
DEVELOPER = "MD ABDULLAH"
EMAIL = "mdabdull0108@gmail.com"
VERSION = "V0.1"

def log_result(data):
    with open("recon_report.txt", "a") as f:
        f.write(f"\n--- SCAN DATA ({time.strftime('%Y-%m-%d %H:%M:%S')}) ---\n")
        f.write(data + "\n")

# --- 1. REVERSE IP LOOKUP ---
def reverse_ip_lookup():
    target = input("\n[+] Enter IP or Domain for Reverse Lookup: ")
    try:
        ip_addr = socket.gethostbyname(target)
        print(f"[*] Fetching domains hosted on: {ip_addr}...")
        url = f"https://api.hackertarget.com/reverseiplookup/?q={ip_addr}"
        res = requests.get(url, timeout=10)
        if res.status_code == 200 and "error" not in res.text.lower():
            print(f"\n[!] DOMAINS FOUND:\n{res.text.strip()}")
            log_result(f"Reverse IP for {ip_addr}:\n{res.text}")
        else:
            print("[-] No other domains found or API limit reached.")
    except Exception as e:
        print(f"[-] Error: {e}")

# --- 2. SQL INJECTION SCANNER (BASIC) ---
def sql_injection_scanner():
    url = input("\n[+] Enter URL with Parameter (e.g., http://site.com/php?id=1): ")
    print("[*] Checking for SQL Injection vulnerability...")
    payloads = ["'", '"', " OR 1=1", " --", " #"]
    vulnerable = False
    for payload in payloads:
        target_url = url + payload
        try:
            res = requests.get(target_url, timeout=5)
            errors = ["mysql", "sql syntax", "mariadb", "oracle", "postgreSQL"]
            if any(error in res.text.lower() for error in errors):
                print(f"  [!!!] VULNERABLE TO SQLi: {target_url}")
                vulnerable = True
                break
        except: pass
    if not vulnerable: print("  [-] No obvious SQLi error detected.")

# --- 3. ROBOTS.TXT & SITEMAP FINDER ---
def hidden_files_finder():
    url = input("\n[+] Enter Target URL: ")
    if not url.startswith("http"): url = "http://" + url
    base_url = "/".join(url.split("/")[:3])
    print(f"[*] Searching hidden files on: {base_url}...")
    for file in ["/robots.txt", "/sitemap.xml", "/sitemap_index.xml"]:
        try:
            res = requests.get(base_url + file, timeout=5)
            if res.status_code == 200:
                print(f"  [!!!] FOUND: {base_url + file}")
        except: pass

# --- 4. CMS & TECHNOLOGY DETECTOR ---
def cms_detector():
    url = input("\n[+] Enter Target URL: ")
    if not url.startswith("http"): url = "http://" + url
    try:
        res = requests.get(url, timeout=10)
        cms = "WordPress" if "wp-content" in res.text else "Joomla" if "joomla" in res.text.lower() else "Unknown"
        server = res.headers.get('Server', 'Hidden')
        print(f"\n[!] CMS: {cms}\n[!] Server: {server}")
        log_result(f"CMS: {cms}, Server: {server}")
    except: print("[-] Connection Error.")

# --- 5. IP GEO-LOCATION (Fixed & Perfect) ---
def geo_location():
    target = input("\n[+] Enter IP or Domain: ")
    try:
        ip_addr = socket.gethostbyname(target)
        res = requests.get(f"http://ip-api.com/json/{ip_addr}").json()
        if res['status'] == 'success':
            loc_info = f"Country: {res['country']}, City: {res['city']}, ISP: {res['isp']}"
            print(f"\n[!] LOCATION: {loc_info}")
            
            lat = res['lat']
            lon = res['lon']
            print(f"[*] Maps: https://www.google.com/maps?q={lat},{lon}")
            
    except Exception as e: 
        print(f"[-] Error: {e}")

# --- 6. SUBDOMAIN ATTACK ---
def subdomain_attack():
    domain = input("\n[+] Enter Domain: ")
    subs = ['www', 'dev', 'admin', 'mail', 'api', 'vpn', 'secure', 'test', 'shop']
    print(f"[*] Scanning Subdomains for {domain}...")
    for s in subs:
        try:
            full = f"{s}.{domain}"
            print(f"  [+] Found: {full} ({socket.gethostbyname(full)})")
        except: pass

# --- MAIN MENU ---
def main():
    while True:
        os.system('clear' if os.name != 'nt' else 'cls')
        print("="*68)
        print(f"   🛡️  ABDULLAH RECON-X {VERSION} | DEVELOPED BY: {DEVELOPER}")
        print(f"   Contact Me :- {EMAIL}")
        print("="*68)
        print("1. Reverse IP Lookup (Find other sites on same IP)")
        print("2. SQL Injection Scanner (Check URL vulnerability)")
        print("3. Find Robots.txt & Sitemap (Hidden Files)")
        print("4. CMS & Technology Detector (WP, Joomla, Server)")
        print("5. IP Geo-Location (Find Country & Google Maps)")
        print("6. Subdomain Dictionary Attack")
        print("7. WHOIS Lookup (Domain Owner Details)")
        print("8. Exit")
        print("="*68)
        
        choice = input("[?] Action (1-8): ")
        if choice == '1': reverse_ip_lookup()
        elif choice == '2': sql_injection_scanner()
        elif choice == '3': hidden_files_finder()
        elif choice == '4': cms_detector()
        elif choice == '5': geo_location()
        elif choice == '6': subdomain_attack()
        elif choice == '7':
            d = input("\nDomain: ")
            try: print(whois.whois(d))
            except: print("[-] WHOIS Error.")
        elif choice == '8': break
        input("\n[DONE] Press Enter to return...")

if __name__ == "__main__":
    main()
