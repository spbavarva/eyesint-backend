import requests
from bs4 import BeautifulSoup

def nameinfo(target):
    def check_username(username, platform_url, not_found_phrase):
        response = requests.get(platform_url.format(username))
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if not_found_phrase in soup.get_text():
            return None
        else:
            return platform_url.format(username)

    def main():
        username = target

        platforms = {
            'Instagram': 'https://www.instagram.com/{}',
            'Facebook': 'https://www.facebook.com/{}',
            'Twitter': 'https://www.twitter.com/{}',
            'YouTube': 'https://www.youtube.com/{}',
            'Blogger': 'https://{}.blogspot.com',
        }

        not_found_phrases = {
            'Instagram': 'The link you followed may be broken,',
            'Facebook': 'The page you requested was not found,',
            'Twitter': 'The page does not exist,',
            'YouTube': 'This page isn’t available,',
            'Blogger': 'HTTP/2 404',
        }

        found_platforms = []

        output = []  # Create an empty list to collect output

        for platform, url in platforms.items():
            result = check_username(username, url, not_found_phrases[platform])
            if result:
                found_platforms.append((platform, result))
                output.append(f"{platform}: {result}")
            else:
                output.append(f"{platform}: Not Found!")

        # Return the collected output as a list
        return output

    # Call the main function and return its result
    return main()

# This part of the script will only be executed when the script is run directly,
# not when it's imported as a module in app.py
if __name__ == "__main__":
    result = nameinfo("your_target_username")
    for line in result:
        print(line)
