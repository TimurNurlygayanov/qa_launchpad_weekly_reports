#!/usr/bin/env python
#
#    Copyright 2015 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import optparse
import urlparse
from xml.etree import ElementTree

import report
from settings import JENKINS
from settings import logger
from settings import TestRailSettings
from testrail_client import TestRailProject


LOG = logger


# Initialize TestRail project client
client = TestRailProject(url=TestRailSettings.url,
                         user=TestRailSettings.user,
                         password=TestRailSettings.password,
                         project=TestRailSettings.project)

tests_suite = client.get_suite_by_name(TestRailSettings.tests_suite)

cases = client.get_cases(tests_suite["id"])
for case in cases:
    print case["custom_qa_team"]
    if case["custom_qa_team"] == "":
        case["custom_qa_team"] = 4
    print "updated:", case["id"]
    client.update_case(case)


