import requests
from bs4 import BeautifulSoup

page = requests.get("https://example.com")
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.title.text)  # Doit afficher "Example Domain"