import requests
import sys
from colorama import Fore, Style

def check_metrics(url):
    try:
        response = requests.get(f"{url}/metrics", timeout=5)
        if response.status_code == 200:
            return url, True
        else:
            return url, False
    except requests.RequestException as e:
        
        print(f"Error connecting to the URL {e}")
        return url, False

def test_urls(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
    
    urls = [url.strip() for url in urls]

    for url in urls:
        url, is_accessible = check_metrics(url)
        if is_accessible:
            print(f"{Fore.GREEN}{url}/metrics")
        else:
            print("")

def main():
    if len(sys.argv) != 2:
        print("Usage: python check_prometheus_metrics.py <input_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]

    test_urls(file_path)

if __name__ == "__main__":
    main()
