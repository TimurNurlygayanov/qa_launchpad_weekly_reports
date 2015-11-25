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


# Initialize TestRail project client
client = TestRailProject(url=TestRailSettings.url,
                         user=TestRailSettings.user,
                         password=TestRailSettings.password,
                         project=TestRailSettings.project)

tests_suite = client.get_suite_by_name(TestRailSettings.tests_suite)

cases = client.get_cases(tests_suite["id"])
for case in cases:
    if case["custom_qa_team"] == "":
        case["custom_qa_team"] = 4  # 4 it is "MOS" group
        print "updated:", case["id"]
        client.update_case(case)
