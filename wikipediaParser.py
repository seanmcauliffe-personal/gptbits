"""
Module for parsing Wikipedia pages.
"""

import re
import requests
import textwrap
from bs4 import BeautifulSoup

def parse_wikipedia_page(page_url):
    """
    Parse the given Wikipedia page and return the cleaned text and the links.

    Args:
        page_url (str): The URL of the Wikipedia page to parse.

    Returns:
        str: The cleaned text from the page.
        list: The links from the page.
    """
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    content = soup.find('div', {'id': 'mw-content-text'})
    paragraphs = content.find_all('p', recursive=False)

    cleaned_text = ""
    for paragraph in paragraphs:
        text = paragraph.get_text().strip()
        # Remove unnecessary whitespace, newlines, etc.
        text = re.sub(r'\s+', ' ', text)
        text = textwrap.fill(text, width=70)
        cleaned_text += text + "\n\n"

    # Extract hyperlinks
    links = [a['href'] for a in content.find_all('a', href=True)]
    links = [page_url + link if link.startswith('/') else link for link in links]

    return cleaned_text, links

wiki_url = "https://en.wikipedia.org/wiki/OpenAI"
parsed_text, parsed_links = parse_wikipedia_page(wiki_url)

print("Cleaned Text:\n", parsed_text)
print("\nLinks:\n", "\n".join(parsed_links))

