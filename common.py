import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def get_text_from_url(url):

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(response.text, "html.parser")

    for p in soup.find_all("p"):
        p.append("\n\n")   # add newline after each <p>

    # Remove unwanted tags
    for tag in soup(["script", "style", "noscript"]):
        tag.extract()

    text = soup.get_text(separator="\n\n", strip=True)

    return text

def get_text_from_html(html):

    soup = BeautifulSoup(html, "html.parser")

    for p in soup.find_all("p"):
        p.append("\n\n")   # add newline after each <p>

    # Remove unwanted tags
    for tag in soup(["script", "style", "noscript"]):
        tag.extract()

    text = soup.get_text(separator="\n\n", strip=True)

    return text
