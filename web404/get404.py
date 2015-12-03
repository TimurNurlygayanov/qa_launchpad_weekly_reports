import re
import sys
from grab import Grab
from progress.bar import Bar


if len(sys.argv) != 3:
    print "Please specify initial URL and domain"
    exit(1)


g = Grab()


SELECTOR = ("//div[not(contains(@style,'display:none')"
            " or contains(@class,'hidden'))]"
            "/*/a[@href[contains(.,'{0}')]]").format(sys.argv[2])


def open_page(url, timeout):
    try:
        page = g.go(url=url, timeout=timeout)
    except Exception:
        print "It takes more {1} seconds to open '{0}'".format(url, timeout)
        return False
    return page


def get_page_childs(parent_url):
    urls = []
    page = open_page(parent_url, 5)

    if page is False:
        return urls

    all_urls = page.select(SELECTOR)
    for url in all_urls:
        link = re.search('href=(\S+)', url.html())
        urls.append({'link': link.group(0).split('"')[1],
                     'parent': parent_url})
    return urls


def get_page_status(page, timeout=5):
    url = page['link']
    if url.startswith('/'):
        url = sys.argv[1] + url
    check = open_page(url, timeout)
    if check is not False and "200 OK" not in check.status:
        print check.status, url, "parent:", page.get('parent')
        return False
    return True


print("Collecting list of child pages... ")
childs = get_page_childs(sys.argv[1])

CACHE = []
new_childs_count = len(childs)
#bar = Bar('Processing', max=len(childs))
#bar.next()
while new_childs_count > 0:
    prev = len(childs)

    new = []
    for page in childs:
        if page['link'] not in CACHE:
            if get_page_status(page):
                CACHE.append(page['link'])
                new += get_page_childs(page['link'])

    childs += new
    #childs = list(set(childs))
    new_childs_count = len(childs) - prev
    #bar.next()
    print("Found {0} new child pages".format(new_childs_count))

#bar.finish()

print("Total count of pages for check: {0}".format(len(childs)))
