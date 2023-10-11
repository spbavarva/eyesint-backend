import requests
import json  # Import the json module
import sys

def domainS(domain):
    api_key = "328c507d19905d6cac7e7842c3a278ac38cb698a"
    url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={api_key}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Request failed with status code {response.status_code}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python domain.py <domain>")
    else:
        domain_to_search = sys.argv[1]
        result = domainS(domain_to_search)
        if result:
            # Pretty-print the JSON data with indentation
            print(json.dumps(result, indent=4))
