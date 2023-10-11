import requests

def number(phonenum):
    result = {}
    
    url = "http://apilayer.net/api/validate"
    params = {
        "access_key": "cd3af5f7d1897dc1707c47d05c3759fd",
        "number": phonenum
    }
    
    resp = requests.get(url, params=params)
    details = resp.json()
    
    result["Country"] = details.get("country_name", "")
    result["Location"] = details.get("location", "")
    result["Carrier"] = details.get("carrier", "")
    
    # Check if the fields are present in the API response and have a value
    if "type" in details and details["type"]:
        result["Number Type"] = details["type"]
    if "valid" in details and details["valid"]:
        result["Validity"] = details["valid"]
    if "line_type" in details and details["line_type"]:
        result["Line Type"] = details["line_type"]
    if "time_zone" in details and details["time_zone"]:
        result["Time Zone"] = details["time_zone"]
    if "international_dialing_code" in details and details["international_dialing_code"]:
        result["International Dialing Code"] = details["international_dialing_code"]
    if "local_number_format" in details and details["local_number_format"]:
        result["Local Number Format"] = details["local_number_format"]
    
    return result

if __name__ == "__main__":
    phonenum = input("Enter phone number: ")
    result = number(phonenum)
    
    # Print only the fields with values
    for key, value in result.items():
        if value:
            print(f"{key}: {value}")
