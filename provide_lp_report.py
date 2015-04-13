import datetime
from dateutil import parser
import pytz
from launchpadlib.launchpad import Launchpad


engineers = ['tnurlygayanov', 'akuznetsova', 'ylobankov', 'vrovachev',
             'esikachev', 'vgusev', 'svasheka', 'ogubanov', 'obutenko',
             'kkuznetsova', 'kromanenko', 'vryzhenkin', 'agalkin']

cachedir = "~/.launchpadlib/cache/"
launchpad = Launchpad.login_anonymously('just testing', 'production', cachedir)

one_week_ago_date = datetime.datetime.now() - datetime.timedelta(weeks=1)

created_on_this_week_total = 0

for engineer in engineers:
    p = launchpad.people[engineer]

    print "\n\n {0} ".format(p.display_name)
    print "-" * 121
    print "| {0}\t\t| {1}\t\t| {2}\t\t| {3}\t\t\t\t\t\t\t|".format("ID", "Status", "Assigned To", "Link")
    print "-" * 121

    list_of_created_bugs = p.searchTasks(bug_reporter=p,
                                         modified_since=one_week_ago_date)
    created_on_this_week = []

    for bug in list_of_created_bugs:
        bug_created_date = bug.date_created.ctime()

        if parser.parse(bug_created_date) > parser.parse(one_week_ago_date.ctime()):
            created_on_this_week.append(bug)

            assigned_to = "None" if not bug.assignee else bug.assignee.name
            if len(assigned_to) < 6:
                assigned_to += "\t"
            if len(assigned_to) < 14:
                assigned_to += "\t"
     
            status = bug.status
            if len(status) < 7:
                status += "\t"
            if len(status) < 14:
                status += "\t"

            web_link = bug.web_link
            if len(web_link) < 45:
                web_link += "\t"

            print "| {0:d}\t| {1:s}\t| {2:s}\t| {3:s}\t|".format(bug.bug.id, status, assigned_to, web_link)
            created_on_this_week_total += 1

    print "-" * 121
    print "Total bugs found during the last week:", len(created_on_this_week)

print "\n\nTotal bugs found during the last week by MOS QA team:", created_on_this_week_total
