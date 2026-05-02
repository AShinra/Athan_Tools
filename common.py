import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# check if url is valid
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

# get text from url
def get_text_from_url(url):
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return f"Request error: {e}"

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove unwanted tags
    for tag in soup(["script", "style", "noscript", "nav", "footer", "header", "aside"]):
        tag.decompose()
    
    # Common content selectors (priority order)
    selectors = [
        ".article__content",
        "main",
        "article",
        "div.content",
        "div#content",
        "section.content",
        ".post-content",
        ".entry-content",
        ".article-body",
        ".post-body"]

    content = None

    # Try each selector
    for selector in selectors:
        content = soup.select_one(selector)
        if content and len(content.get_text(strip=True)) > 200:  # ensure it's meaningful
            break

    # Fallback to body if nothing found
    if not content:
        content = soup.body

    # Add spacing after paragraphs
    for p in content.find_all("p"):
        p.append("\n\n")

    text = content.get_text(separator="\n\n", strip=True)

    return text, content.prettify()

# get text from html input
def get_text_from_html(html):

    soup = BeautifulSoup(html, "html.parser")

    for p in soup.find_all("p"):
        p.append("\n\n")   # add newline after each <p>

    # Remove unwanted tags
    for tag in soup(["script", "style", "noscript"]):
        tag.extract()

    text = soup.get_text(separator="\n\n", strip=True)

    return text


