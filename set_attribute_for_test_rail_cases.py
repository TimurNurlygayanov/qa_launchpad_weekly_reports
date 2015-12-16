#!/usr/bin/env python
#
# HOW TO RUN THIS SCRIPT
# 1. Check code of your team in TestRail
# 2. Read text of this script carefully
# 3. If you want to use this script, update it
#    accordingly to your needs
# 4. Run:
#     export TESTRAIL_USER='<your_user>'
#     export TESTRAIL_PASSWORD='your_password'
#     export TESTRAIL_MILESTONE='8.0'
#     export TESTRAIL_TEST_SUITE=""
#     export RELEASE='Ubuntu 14.04'
#

from settings import TestRailSettings
from testrail_client import TestRailProject


milestone = "8.0"
team = "MOS"
test_case_type = "manual"
complexity = "core"

milestones = {"7.0": 9, "8.0": 10, "6.1": 4, "6.0": 5, "5.1.1": 8,
              "5.1.2": 7, "6.0.1": 6}
qa_teams = {"MOS": 4, "Fuel": 2, "Maintenance": 3, "Framework-CI": 1,
            "Performance": 5, "PCE": 6, "Telco": 7}
complexity_types = {"core": 2, "smoke": 1, "advanced": 3}
types = {"automated": 1, "manual": 7}

# Initialize TestRail project client
client = TestRailProject(url=TestRailSettings.url,
                         user=TestRailSettings.user,
                         password=TestRailSettings.password,
                         project=TestRailSettings.project)

tests_suite = client.get_suite_by_name(TestRailSettings.tests_suite)

cases = client.get_cases(tests_suite["id"])
for case in cases:
    #if case["id"] == 542603:
    #    print case
    #continue

    need_update = False

    if case["custom_qa_team"] != qa_teams[team]:
        case["custom_qa_team"] = 4
        need_update = True

    if case["milestone_id"] != milestones[milestone]:
        case["milestone_id"] = milestones[milestone]
        need_update = True

    if case["type_id"] != types[test_case_type]:
        case["type_id"] = types[test_case_type]
        need_update = True

    if case["custom_case_complexity"] != complexity_types[complexity]:
        case["custom_case_complexity"] = complexity_types[complexity]
        need_update = True

    if not case["custom_test_case_steps"]:
        case["custom_test_case_steps"]: [{u'content': u'/', u'expected': u'/'}]
        need_update = True

    if need_update:
        print "updated:", case["id"]
        client.update_case(case)
