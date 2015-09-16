"""
(tnurlygayanov) The main goal of this script is to simplify the life of
                people who are working with QA reports.
"""

from datetime import datetime
from datetime import timedelta
from grab import Grab


DAYS = 10
HOST = 'http://lp-reports.vm.mirantis.net'
VERSION = 'milestone=7.0'
URL = '{0}/reports/custom_report?{1}&{2}_from={3}&{2}_to={4}{5}'
COLLECTOR = '//a[starts-with(@href, "#") and string-length(@href) > 3]'
g = Grab()


def get_count_of_bugs(HOST, VERSION, OPERATION, DATE_FROM, DATE_TO, PRIORITY):
    page = g.go(url=URL.format(HOST, VERSION, OPERATION, DATE_FROM,
                               DATE_TO, PRIORITY),
                timeout=10)
    objects = page.select(COLLECTOR)

    count_of_bugs = 0
    for i in xrange(1, page.select(COLLECTOR).count()):
        item = page.select(COLLECTOR + '[{0}]'.format(i)).text()
        count_of_bugs += int(item.split(': ')[1])

    return count_of_bugs


for d in xrange(1, DAYS+1):
    DATE_FROM = datetime.today().date() - timedelta(days=DAYS-d)
    DATE_FROM_OLD = datetime.today().date().replace(DATE_FROM.year - 5)
    DATE_TO = datetime.today().date() - timedelta(days=DAYS-d-1)

    print "-"*100
    print "DATE: ", DATE_FROM

    for t in [{"date": DATE_FROM, "type": "New"},
              {"date": DATE_FROM_OLD, "type": "Total"}]:
        for p in [{'priority': '', 'filter': ''},
                  {'priority': 'Critical+High',
                   'filter': '&importance=Critical&importance=High'}]:
            count_of_bugs = get_count_of_bugs(HOST, VERSION, 'fix_committed',
                                              t['date'], DATE_TO, p['filter'])
            print t['type'], p['priority'], "Fix Commited:", count_of_bugs

            count_of_bugs = get_count_of_bugs(HOST, VERSION, 'fix_released',
                                              t['date'], DATE_TO, p['filter'])
            print t['type'], p['priority'],"Fix Released:", count_of_bugs
