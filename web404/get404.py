import configparser
import re
import sys
from grab import Grab
from progress.bar import Bar


g = Grab()
config = configparser.ConfigParser()
config.read('server.conf')
initial_url = config['DEFAULT'].get('initial_url', 'google.com')
host = config['DEFAULT'].get('child_urls_should_contain', '')
timeout = config['DEFAULT'].get('timeout', 5)
results_file = config['DEFAULT'].get('results_file', 'results.txt')
exclude_urls = config['DEFAULT'].get('exclude_urls', '').split('\n')

print exclude_urls

SELECTOR = ("//div[not(contains(@style,'display:none')"
            " or contains(@class,'hidden'))]"
            "/*/a[@href[contains(.,'{0}')]]").format(host)


def write_result(string):
    with open(results_file, 'a+') as f:
        f.write(string + "\n")


def open_page(url):
    try:
        page = g.go(url=url)
    except Exception:
        write_result("It takes more {0} seconds to open '{1}'"
                     .format(timeout, url))
        return False
    return page


def get_page_childs(parent_url):
    urls = []
    page = open_page(parent_url)

    if page is False:
        return urls

    all_urls = page.select(SELECTOR)
    for url in all_urls:
        link = re.search('href=(\S+)', url.html())
        urls.append({'link': link.group(0).split('"')[1],
                     'parent': parent_url})
    return urls


def get_page_status(page):
    url = page['link']
    if url.startswith('/'):
        url = sys.argv[1] + url
    check = open_page(url)
    if check is not False and "200 OK" not in check.status:
        write_result("{0} {1} parent page: {2}".format(check.status, url,
                                                       page.get('parent')))
        return False
    return True


print("Collecting list of child pages... ")
childs = get_page_childs(initial_url)

CACHE = []
new_childs_count = len(childs)
bar = Bar('Processing', max=len(childs))

while new_childs_count > 0:
    prev = len(childs)
    new = []
    for page in childs:
        if page['link'] not in CACHE:
            bar.max = len(new) + prev
            bar.next()
            for url in exclude_urls:
                if url in page['link']:
                    continue
            if get_page_status(page):
                CACHE.append(page['link'])
                new += get_page_childs(page['link'])

    childs += new
    new_childs_count = len(childs) - prev

bar.finish()

with open("all_tested_links", 'a+') as f:
    for page in childs:
        f.write(page['link'] + "\n")
