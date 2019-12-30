import json
import requests
from collections import Counter
from bs4 import BeautifulSoup


URL = 'https://pikabu.ru'
cookie = input('Введите куки: ')
HEADERS = {'Cookie': cookie,
          'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) '
                        'Gecko/20100101 Firefox/71.0'}


def get_100_posts():
    """ Returns 100 subscription posts from the URL. """
    with requests.Session() as s:
        page = 0
        all_posts = []
        while len(all_posts) < 100:
            get_page = s.get(f'{URL}/new/subs?page={page}', headers=HEADERS)
            soup = BeautifulSoup(get_page.text, "html.parser")
            all_posts.extend(soup.findAll('article')[:9])
            page += 1
        return all_posts[:99]


def count_tags(posts, tags_container=[]):
    """ Returns a list of all tags. """
    for every_post in posts:
        tags_container.extend(every_post.findAll('a', class_="tags__tag"))
    all_tags = [i.get('data-tag')for i in tags_container
                if i.get('data-tag') is not None]
    return all_tags


def write_top_10_tags(all_tags):
    """ Sorts 10 most common tags and writes them into a dictionary. """
    count = dict(Counter(all_tags).most_common(10))
    with open('tags_count.json', 'w') as wf:
        json.dump(count, wf, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    posts = get_100_posts()
    statistics = count_tags(posts)
    write_top_10_tags(statistics)
