import socket
import ipwhois

def clean_url(url):
    # Remove 'https://'
    if url.startswith('https://'):
        url = url[len('https://'):]

    # Remove trailing '/'
    if url.endswith('/'):
        url = url[:-1]

    return url

def get_ip_address(url):
    try:
        ip_address = socket.gethostbyname(clean_url(url))
        return ip_address
    except socket.gaierror:
        return None

def whois_lookup(url):
    ip_address = get_ip_address(url)
    result = {}

    if ip_address is not None:
        try:
            lookup = ipwhois.IPWhois(ip_address)
            results = lookup.lookup_rdap()
            
            # Populate the result dictionary with top-level attributes
            for key, val in results.items():
                if val is not None and not isinstance(val, dict):
                    temp_val = str(val).replace(',', ' ').replace('\r', ' ').replace('\n', ' ')
                    result[key] = temp_val
            
            # Populate the result dictionary with attributes within 'network' dictionary
            network_info = results.get('network')
            if network_info is not None and isinstance(network_info, dict):
                for key, val in network_info.items():
                    if val is not None:
                        temp_val = str(val).replace(',', ' ').replace('\r', ' ').replace('\n', ' ')
                        result[key] = temp_val
            
        except Exception as e:
            result['Error'] = str(e)
    
    else:
        result['Error'] = f'Could not get IP address for URL: {url}'
    
    return result

if __name__ == '__main__':
    url = 'https://www.bvmengineering.ac.in/'  # Include 'https://' prefix and trailing '/'
    result = whois_lookup(url)
    # print(result)  # You can use this result in your frontend
