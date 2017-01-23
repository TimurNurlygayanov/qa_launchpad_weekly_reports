#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# Note: many tests will fail because of two bugs,
#       which were identified during the test design / execution:
#       1) MAX element ID is 9223372036854775807, and any other ID,
#          which is larger than this number will be replaced to this
#          maximum allowed number (Minor priority bug).
#       2) The most part of endpoins allow send POST/PUT/DELETE/UPDATE
#          requests, but only GET method is allowed for these endpoints [1].
#          (High priority bug).
#
# [1] http://api.rutracker.org/v1/docs/

import pytest
import requests

from test_variables import ENDPOINTS, MAX_LIMIT


LARGE_ID = '10000000000000000000000000000'

CHECK_ENDPOINTS = [
    ('topic_id', ENDPOINTS['get_tor_hash']),
    ('topic_id', ENDPOINTS['get_peer_stats']),
    ('user_id', ENDPOINTS['get_user_torrents']),
    ('user_id', ENDPOINTS['get_user_name']),
    ('forum_id', ENDPOINTS['get_forum_data']),
    ('forum_id', ENDPOINTS['get_forum_name']),
    ('topic_id', ENDPOINTS['get_tor_hash']),
    ('hash', ENDPOINTS['get_topic_id']),
    ('topic_id', ENDPOINTS['get_tor_topic_data'])
]


@pytest.mark.negative
@pytest.mark.parametrize("method", ['POST', 'PUT', 'DELETE', 'UPDATE'])
@pytest.mark.parametrize("endpoint", ENDPOINTS.values())
def test_check_different_rest_methods(method, endpoint):
    """ Test checks different methods of requests to all endpoints
        (only GET requests are described in the documentation,
         other methods shouldn't be allowed).
    """

    error_msg = "Method {0} shouldn't be allowed for the edpoint '{1}'."
    error_msg = error_msg.format(method, endpoint)

    if '{0}' in endpoint:
        endpoint = endpoint.format(7)

    r = requests.request(method, endpoint)

    assert r.status_code == 405, error_msg


@pytest.mark.negative
@pytest.mark.parametrize('by,endpoint', CHECK_ENDPOINTS)
def test_get_many_elements(by, endpoint):
    """ Test checks that we can't get more than MAX_LIMIT elements. """

    err_msg = "API should return error message."

    ids = [str(i) for i in xrange(MAX_LIMIT + 1)]

    search_params = {'by': by, 'val': ','.join(ids)}
    r = requests.get(endpoint, params=search_params)
    data = r.json()

    text = 'param [val] is over the limit of {0} (you sent {1} values)'
    expected_data = {'error': {'text': text.format(MAX_LIMIT, MAX_LIMIT + 1),
                               'code': 1}}

    assert data == expected_data, err_msg


@pytest.mark.negative
@pytest.mark.parametrize('by,endpoint', CHECK_ENDPOINTS)
@pytest.mark.parametrize('wrong_id,expected_data', [
    ('-100', ('result', '-100', None)),
    (LARGE_ID, ('result', LARGE_ID, None)),
    ('TEST', ('error', 'text', 'param [val] is empty')),
    ('*', ('error', 'text', 'param [val] is empty')),
    ('& A!', ('error', 'text', 'param [val] is empty')),
    ('', ('error', 'text', 'param [val] is empty')), ])
def test_get_elements_with_wrong_id(by, endpoint, wrong_id, expected_data):
    """ Test checks that we can't get elements using incorrect id. """

    err_msg = ("API should return '{0}' for incorrect element ID '{1}',"
               " but it returns {2} instead.")

    search_params = {'by': by, 'val': wrong_id}
    key1, key2, expected_value = expected_data

    # we have different endpoint and error message for 'get_forum' function:
    if '/pvc/f/' in endpoint:
        endpoint = endpoint.format(wrong_id)
        key1, key2, expected_value = 'error', 'text', 'HTTP Error 404'
        search_params = None

    # we have different error message for search by hash:
    if by == 'hash':
        key1, key2 = 'error', 'text'
        expected_value = 'invalid hash: {0}'.format(wrong_id)

    # for function 'get_user_torrents' we have different default value:
    if 'get_user_torrents' in endpoint and key1 == 'result':
        expected_value = []

    # try to get the element with wrong id:
    r = requests.get(endpoint, params=search_params)
    data = r.json()

    err_msg = err_msg.format(expected_value, wrong_id, data)

    # verify that we got expected error message:
    assert data.get(key1, {}).get(key2, '') == expected_value, err_msg
