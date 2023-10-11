import pdfplumber
import re

R = '\033[1;31;40m'
G = '\033[1;32;40m'
C = '\033[1;36;40m'
Y = '\033[1;33;40m'

def parse_date(date_str):
    # Extract date components using regular expressions
    match = re.match(r'D:(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})([+-])(\d{2})\'(\d{2})\'', date_str)
    if match:
        year, month, day, hour, minute, second, tz_sign, tz_hour, tz_minute = match.groups()
        
        # Convert to a human-readable format
        formatted_date = f"{day} : {month} : {year} {hour}:{minute}:{second}"
        
        # Account for the timezone offset
        if tz_sign == '+':
            formatted_date += f" UTC+{tz_hour}:{tz_minute}"
        elif tz_sign == '-':
            formatted_date += f" UTC-{tz_hour}:{tz_minute}"
        
        return formatted_date
    else:
        return date_str  # Return the original string if parsing fails

def pdfinfo(file_path):
    with pdfplumber.open(file_path) as pdf:
        metadata = pdf.metadata
        metadata_dict = {}
        if metadata:
            for key, value in metadata.items():
                key = key.capitalize()
                if key == 'Creationdate' or key == 'Moddate':
                    formatted_date = parse_date(value)
                    metadata_dict[key] = formatted_date
                else:
                    metadata_dict[key] = value
        return metadata_dict


