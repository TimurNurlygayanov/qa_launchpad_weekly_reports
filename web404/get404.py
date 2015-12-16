import configparser
import re
import time
from grab import Grab
from progress.bar import Bar
from multiprocessing import Process, Queue


def write_result(string):
    with open(results_file, 'a+') as f:
        f.write(string.encode("utf-8", "replace") + "\n")


def open_page(virtual_browser, url):
    try:
        page = virtual_browser.go(url=url)
    except Exception:
        write_result("It takes more then {0} seconds to open '{1}'"
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
        link = link.group(0).split('"')[1]
        if link.startswith('/'):
            link = parent_url + link

        urls.append({'link': link, 'parent': parent_url})
    return urls


def get_page_status(page):
    url = page['link']

    for bad_url in exclude_urls:
        if bad_url in url:
            return False

    virtual_browser = Grab()
    check = open_page(virtual_browser, url)
    if check is not False and "200 OK" not in check.status:
        write_result(unicode("{0} {1} parent page: {2}")
                     .format(unicode(check.status),
                             unicode(url),
                             unicode(page.get('parent'))))
        return False
    return True


def collect_childs(queue, results):
    new = []
    if not queue.empty():
        page = queue.get(timeout=1)
        if get_page_status(page):
            new = get_page_childs(page['link'])
        results.put(new, timeout=10)


config = configparser.ConfigParser()
config.read('server.conf')
initial_url = config['DEFAULT'].get('initial_url', 'google.com')
host = config['DEFAULT'].get('child_urls_should_contain', '707')
timeout = config['DEFAULT'].get('timeout', 5)
results_file = config['DEFAULT'].get('results_file', 'results.txt')
exclude_urls = config['DEFAULT'].get('exclude_urls', '707').split('\n')
max_threads_count = int(config['DEFAULT'].get('max_threads_count', 20))
max_recursion = int(config['DEFAULT'].get('max_recursion', 3))

SELECTOR = ("//*[not(contains(@style,'display:none')"
            " or contains(@class,'hidden'))]"
            "/*/a[contains(@href,'{0}')"
            " or starts-with(@href,'/')]").format(host)

childs = get_page_childs(initial_url)
CACHE = []
new_pages_count = len(childs)
bar = Bar('Processing', max=len(childs))
bar.start()
recursion = 0

while new_pages_count > 0:
    queue = Queue()
    results_queue = Queue()
    new_pages_count = 0

    for page in childs:
        if page['link'] not in CACHE:
            CACHE.append(page['link'])
            queue.put(page, timeout=10)
            time.sleep(0.01)
            new_pages_count += 1

    done = 0
    bar.max = len(CACHE)

    while not queue.empty():
        threads_count = 1 + (new_pages_count - done) / 2

        if threads_count > max_threads_count:
            threads_count = max_threads_count

        workers = [Process(target=collect_childs, args=(queue, results_queue))
                   for i in xrange(threads_count)]
        for w in workers:
            w.daemon = True
        [w.start() for w in workers]

        for w in workers:
            w.join(timeout=0.1)
            for _ in xrange(results_queue.qsize() - done):
                bar.next()
                done += 1

    recursion += 1
    if recursion > max_recursion:
        break

    while not results_queue.empty():
        childs += results_queue.get()

bar.finish()

with open("all_tested_links", 'a+') as f:
    for page in CACHE:
        f.write(page + "\n")
