import ssl
import OpenSSL
import sys
import socket
import datetime
import pytz


def convert_asn1_time(asn1_time):
    timestamp = asn1_time.decode("utf-8")
    dt = datetime.datetime.strptime(timestamp, "%Y%m%d%H%M%SZ")
    dt_utc = pytz.utc.localize(dt)
    return dt_utc.strftime("%d %B %Y %H:%M:%S %Z")

def clean_url(target):
    # Remove 'https://'
    if target.startswith('https://'):
        target = target[len('https://'):]

    # Remove trailing '/'
    if target.endswith('/'):
        target = target[:-1]

    return target

def get_ip_address(target):
    try:
        ip_address = socket.gethostbyname(clean_url(target))
        return ip_address
    except socket.gaierror:
        return None

def ssl_analyzer(target):
    ip_address = get_ip_address(target)

    if target.startswith("http://"):
        target = target[len("http://"):]
    elif target.startswith("https://"):
        target = target[len("https://"):]

    result = []
    result.append('\nSSL Certificate Analysis:\n')
    result.append(f'IP address : {ip_address}')

    try:
        cert = ssl.get_server_certificate((ip_address, 443))
        x509 = OpenSSL.crypto.load_certificate(
            OpenSSL.crypto.FILETYPE_PEM, cert)
        
        valid_from = convert_asn1_time(x509.get_notBefore())
        valid_until = convert_asn1_time(x509.get_notAfter())

        valid_from_date = datetime.datetime.strptime(valid_from, "%d %B %Y %H:%M:%S %Z")
        valid_until_date = datetime.datetime.strptime(valid_until, "%d %B %Y %H:%M:%S %Z")

        days_difference = (valid_until_date - valid_from_date).days

        result.append(f'Valid from: {valid_from}')
       

        result.append(f'Valid until: {valid_until}')

        result.append(f'Days Difference: {days_difference} days')
        result.append(f'Expired: {x509.has_expired()}')
        result.append(f'Signature Algorithm: {x509.get_signature_algorithm()}')

        for item in x509.get_subject().get_components():
            result.append(f'Subject {item[0]}: {item[1]}')

        result.append(f'Subject Hash: {x509.get_subject().hash()}')

        for item in x509.get_issuer().get_components():
            result.append(f'Issuer {item[0]}: {item[1]}')

        result.append(f'Issuer Hash: {x509.get_issuer().hash()}')

        for i in range(x509.get_extension_count()):
            ext_name = x509.get_extension(i).get_short_name()
            ext_value = x509.get_extension(i).__str__()
            result.append(f'Extension {ext_name}: {ext_value}')

        result.append(f'\nPublic Key Bits: {x509.get_pubkey().bits()}')
        result.append(f'Public Key Type: {x509.get_pubkey().type()}')
        result.append(f'Public Key only public: {x509.get_pubkey()._only_public}')
        result.append(f'Public Key initialized: {x509.get_pubkey()._initialized}')

        serial_number = x509.get_serial_number()
        result.append(f'Serial Number: {serial_number}')
        result.append(f'Serial Number Length: {serial_number.bit_length()}')

        result.append(f'\nMD5: {x509.digest("md5")}')
        result.append(f'SHA1: {x509.digest("sha1")}')
        result.append(f'SHA256: {x509.digest("sha256")}')
        result.append(f'SHA512: {x509.digest("sha512")}')
        # 
        

      

        # result.append(f'\nValid from: {x509.get_notBefore()}')
        # result.append(f'Valid until: {x509.get_notAfter()}')

        result.append('exported: False')

    except Exception as e:
        result.append(f'Exception: {e}')

    return result

if __name__ == "__main__":
    url = 'https://www.bvmengineering.ac.in/'  # Include 'https://' prefix and trailing '/'
    result = ssl_analyzer(url)
    for item in result[2:]:
        print(item)  # You can use this result in your frontend
