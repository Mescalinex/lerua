import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def parseHandler(url, ListSelector, textSelector, LinkSelector):
    url = 'https://leroymerlin.ru/catalogue/'
    result = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    cards = soup.select(ListSelector)
    unreadCnt = 0
    for elem in cards:
        try:
            _dict = {}
            _dict['text'] = elem.select_one(textSelector).text
            _dict['link'] = urljoin(url, elem.select_one(LinkSelector).get('href'))
            result.append(_dict)
        except Exception:
            unreadCnt += 1

    print('unread {} rows'.format(unreadCnt))
    return result