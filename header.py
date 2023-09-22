import requests

def headers(target):
    result = {}
    print(f'\nHeaders :\n')
    try:
        rqst = requests.get(target, verify=False, timeout=10)
        for key, val in rqst.headers.items():
            print(f'{key} : {val}')
            
            result.update({key: val})
    except Exception as e:
        print(f'\nException : {e}\n')
        
        result.update({'Exception': str(e)})     
    
    return result