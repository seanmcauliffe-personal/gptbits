from bs4 import BeautifulSoup
import requests
import re
import textwrap

def parse_wikipedia_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    content = soup.find('div', {'id': 'mw-content-text'})
    paragraphs = content.find_all('p', recursive=False)

    cleaned_text = ""
    for p in paragraphs:
        text = p.get_text().strip()
        # Remove unnecessary whitespace, newlines, etc.
        text = re.sub(r'\s+', ' ', text)
        text = textwrap.fill(text, width=70)
        cleaned_text += text + "\n\n"

    # Extract hyperlinks
    links = [a['href'] for a in content.find_all('a', href=True)]
    links = [url + link if link.startswith('/') else link for link in links]

    return cleaned_text, links

url = "https://en.wikipedia.org/wiki/OpenAI"
text, links = parse_wikipedia_page(url)

print("Cleaned Text:\n", text)
print("\nLinks:\n", "\n".join(links))
