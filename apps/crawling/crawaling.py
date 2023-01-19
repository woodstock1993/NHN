import requests
from bs4 import BeautifulSoup as BP

def get_last_page(url):
    html = requests.get(url)
    soup = BP(html.text, "html.parser")
    pages = soup.find('div', {'class' : 's-pagination'}).find_all('a', {'title': True})
    pages = int(pages[-2].find('span').string)
    return pages