import configparser
import re
from grab import Grab
from progress.bar import Bar
from multiprocessing import Queue
from threading import Thread


config = configparser.ConfigParser()
config.read('server.conf')
initial_url = config['DEFAULT'].get('initial_url', 'google.com')
host = config['DEFAULT'].get('child_urls_should_contain', '')
timeout = config['DEFAULT'].get('timeout', 5)
results_file = config['DEFAULT'].get('results_file', 'results.txt')
exclude_urls = config['DEFAULT'].get('exclude_urls', '').split('\n')
max_threads_count = int(config['DEFAULT'].get('max_threads_count', 20))

SELECTOR = ("//div[not(contains(@style,'display:none')"
            " or contains(@class,'hidden'))]"
            "/*/a[@href[contains(.,'{0}')]]").format(host)


def write_result(string):
    with open(results_file, 'a+') as f:
        f.write(string + "\n")


def open_page(virtual_browser, url):
    try:
        page = virtual_browser.go(url=url)
    except Exception:
        write_result("It takes more {0} seconds to open '{1}'"
                     .format(timeout, url))
        return False
    return page


def get_page_childs(parent_url):
    virtual_browser = Grab()
    urls = []
    page = open_page(virtual_browser, parent_url)

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
        url = host + url

    for bad_url in exclude_urls:
        if bad_url in url:
            return False

    virtual_browser = Grab()
    check = open_page(virtual_browser, url)
    if check is not False and "200 OK" not in check.status:
        write_result("{0} {1} parent page: {2}".format(check.status, url,
                                                       page.get('parent')))
        return False
    return True


class Worker(Thread):
    new = []

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        new = []
        page = self.queue.get()
        if get_page_status(page):
            new = get_page_childs(page['link'])
        Worker.new.extend(new)


childs = get_page_childs(initial_url)
CACHE = []
new_childs_count = len(childs)
bar = Bar('Processing', max=len(childs))
queue = Queue()

while new_childs_count > 0:
    prev = len(childs)
    bar.max = len(childs)

    threads_count = (prev - len(CACHE)) / 10
    if threads_count > max_threads_count:
        threads_count = max_threads_count

    workers = [Worker(queue) for i in xrange(threads_count)]
    [w.start() for w in workers]

    for page in childs:
        if page['link'] not in CACHE:
            CACHE.append(page['link'])
            queue.put(page)
            bar.next()

    [w.join() for w in workers]
    childs += Worker.new
    new_childs_count = len(childs) - prev

bar.finish()

with open("all_tested_links", 'a+') as f:
    for page in childs:
        f.write(page['link'] + "\n")
