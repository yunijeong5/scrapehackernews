import requests
from bs4 import BeautifulSoup
import pprint
from time import time


def performance(fn):
    def wrapper(*args, **kwargs):
        t1 = time()
        result = fn(*args, **kwargs)
        t2 = time()
        print(f'took {t2-t1} ms.')
        return result
    return wrapper

# res = requests.get('https://news.ycombinator.com/news')
# res.text prints HTML file (string)
# BeutifulSoup allows converting this string
# into an object we can work with.

# res = requests.get('https://news.ycombinator.com/news')
# soup = BeautifulSoup(res.text, 'html.parser')
# links = soup.select('.storylink')
# subtexts = soup.select('.subtext')


def sort_stories_by_votes(hn):
    return sorted(hn, key=lambda k: k['votes'], reverse=True)


def create_custom_hn(links, subtexts):
    hn = []
    for idx, item in enumerate(links):
        title = links[idx].getText()
        href = links[idx].get('href', None)
        vote = subtexts[idx].select('.score')

        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points >= 100: # only choose stories with 100+ votes
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)


# pprint.pprint(create_custom_hn(links, subtexts))

@performance
def get_multi_page_hn(page_limit=3):
    page = 1
    news = []
    # mega_links = ''
    # mega_subtexts = ''
    while page <= page_limit:
        url = f'https://news.ycombinator.com/news?p={page}'
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.select('.storylink')
        subtexts = soup.select('.subtext')

        news.extend(create_custom_hn(links, subtexts))
        page += 1

    return news


@performance
def get_multi_page_hn_mega(page_limit=3):
    page = 1
    mega_links = ''
    mega_subtexts = ''
    while page <= page_limit:
        url = f'https://news.ycombinator.com/news?p={page}'
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.select('.storylink')
        subtexts = soup.select('.subtext')

        if page == 1:
            mega_links = links
            mega_subtexts = subtexts
        else:
            mega_links += links
            mega_subtexts += subtexts

        page += 1

    return create_custom_hn(mega_links, mega_subtexts)


# pprint.pprint(get_multi_page_hn(2))
get_multi_page_hn(3)
get_multi_page_hn_mega(3)
