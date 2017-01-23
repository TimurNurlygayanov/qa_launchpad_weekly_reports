#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import requests


HOST = 'http://api.rutracker.org/v1{0}'
ENDPOINTS = {
    'test_error_response': HOST.format('/dbg/test_error_response'),
    'cat_forum_tree': HOST.format('/static/cat_forum_tree'),
    'get_forum': HOST.format('/static/pvc/f/{0}'),
    'get_limit': HOST.format('/get_limit'),
    'get_tor_status_titles': HOST.format('/get_tor_status_titles'),
    'get_forum_name': HOST.format('/get_forum_name'),
    'get_forum_data': HOST.format('/get_forum_data'),
    'get_user_name': HOST.format('/get_user_name'),
    'get_peer_stats': HOST.format('/get_peer_stats'),
    'get_user_torrents': HOST.format('/get_user_torrents'),
    'get_tor_hash': HOST.format('/get_tor_hash'),
    'get_topic_id': HOST.format('/get_topic_id'),
}


def test_check_error_response():
    """ Test checks default error code 503. """

    r = requests.get(ENDPOINTS['test_error_response'])

    assert r.status_code == 503


def test_check_get_forums_tree_cat():
    """ Test checks that all categories are presented
        in list of forums.
    """

    r = requests.get(ENDPOINTS['cat_forum_tree'])
    data = r.json()
    missed_categories = []

    for cat in data['result']['c']:
        if cat not in data['result']['tree']:
            missed_categories.append(cat)

    assert missed_categories == []


def test_check_get_forums_tree_cat_count():
    """ Test checks count of categories in the list of
        categories and the full list of forums.
    """

    r = requests.get(ENDPOINTS['cat_forum_tree'])
    data = r.json()

    cat_count = len(data['result']['c'])
    cat_tree_count = len(data['result']['tree'])

    assert cat_count == cat_tree_count 


def test_check_get_forums_tree_forums():
    """ Test checks that all forums are presented
        in the list of forums.
    """

    r = requests.get(ENDPOINTS['cat_forum_tree'])
    data = r.json()
    forums = data['result']['f']
    missed_forums = []

    for category in data['result']['tree']:
        for forum in data['result']['tree'][category]:
            for subforum in data['result']['tree'][category][forum]:
                if str(subforum) not in forums:
                    missed_forums.append(str(subforum))

    assert missed_forums == []


def test_check_get_forums_tree_forums_count():
    """ Test checks count of forums in the list of
        forums and the full list of forums.
    """

    r = requests.get(ENDPOINTS['cat_forum_tree'])
    data = r.json()
    forums_count = len(data['result']['f'])
    tree_forums_count = 0

    for category in data['result']['tree']:
        tree_forums_count += len(data['result']['tree'][category])
        for forum in data['result']['tree'][category]:
            tree_forums_count += len(data['result']['tree'][category][forum])

    assert forums_count == tree_forums_count


def test_check_get_each_forum():
    """ Test checks that we can get forum by it's id. """

    r = requests.get(ENDPOINTS['get_forum'].format(7))
    data = r.json()

    assert len(data['result']) > 0


def test_get_limit():
    """ Test checks that we have right limit. """

    r = requests.get(ENDPOINTS['get_limit'])
    data = r.json()

    assert data['result']['limit'] == 100


def test_get_tor_status_titles():
    """ Test checks the list of available statuses for topics. """

    r = requests.get(ENDPOINTS['get_tor_status_titles'])
    data = r.json()

    expected_statuses = {'0': u'не проверено', '1': u'закрыто',
                         '2': u'проверено', '3': u'недооформлено',
                         '4': u'не оформлено', '5': u'повтор',
                         '6': u'закрыто правообладателем', '7': u'поглощено',
                         '8': u'сомнительно', "9": u'проверяется',
                         '10': u'временная', '11': u'премодерация'}
    assert data['result'] == expected_statuses


def test_get_forum_name():
    """ Test checks that we can get name of the forum by it's id. """

    search_params = {'by': 'forum_id', 'val': '7'}
    r = requests.get(ENDPOINTS['get_forum_name'], params=search_params)
    data = r.json()

    assert data['result']['7'] == u'Зарубежное кино'


def test_get_forum_name_for_many_forums():
    """ Test checks that we can get name of the forums by their ids. """

    r = requests.get(ENDPOINTS['cat_forum_tree'])
    data = r.json()
    all_forums = data['result']['f']

    # get first 100 elements of dict:
    forums = {k: all_forums[k] for k in all_forums.keys()[:100]}

    search_params = {'by': 'forum_id', 'val': ','.join(forums.keys())}
    r = requests.get(ENDPOINTS['get_forum_name'], params=search_params)
    data = r.json()

    assert data['result'] == forums


def test_get_forum_data():
    """ Test checks that we can get forum's data by it's id. """

    search_params = {'by': 'forum_id', 'val': '7'}
    r = requests.get(ENDPOINTS['get_forum_data'], params=search_params)
    data = r.json()

    expected_data = {'forum_name': u'Зарубежное кино',
                     'parent_id': 0}

    assert data['result']['7'] == expected_data


def test_get_forum_data_for_many_forums():
    """ Test checks that we can get forum's data by ids. """

    r = requests.get(ENDPOINTS['cat_forum_tree'])
    data = r.json()
    res = dict()
    ids_list = list()

    # get dict with subforums and their parents:
    for category in data['result']['tree']:
        for forum in data['result']['tree'][category]:
            for subforum in data['result']['tree'][category][forum]:
                res[str(subforum)] = int(forum)
                ids_list.append(str(subforum))

    ids_string = ','.join(ids_list[:100])

    # get info about names of subforums:
    search_params = {'by': 'forum_id', 'val': ids_string}
    r = requests.get(ENDPOINTS['get_forum_name'], params=search_params)
    data = r.json()

    # generate dict for verification:
    forums_data = dict()
    for forum_id, forum_name in data['result'].iteritems():
        forums_data[str(forum_id)] = {'forum_name': forum_name,
                                      'parent_id': res[str(forum_id)]}

    search_params = {'by': 'forum_id', 'val': ids_string}
    r = requests.get(ENDPOINTS['get_forum_data'], params=search_params)
    data = r.json()

    assert data['result'] == forums_data


def test_get_user_name():
    """ Test checks that we can get names of users by their ids. """

    search_params = {'by': 'user_id', 'val': '2,676767,25856984'}
    r = requests.get(ENDPOINTS['get_user_name'], params=search_params)
    data = r.json()

    expected_data = {'2': 'admin',
                     '676767': 'figley',
                     '25856984': 'do31415926'}

    assert data['result'] == expected_data


def test_get_user_torrents():
    """ Test checks that we can get torrents which were created
        by some user.
    """

    search_params = {'by': 'user_id', 'val': '6477978'}
    r = requests.get(ENDPOINTS['get_user_torrents'], params=search_params)
    data = r.json()

    assert len(data['result']) > 0


def test_get_topic_data_by_id():
    """ Test checks we can get topic data by it's id. """

    r = requests.get(ENDPOINTS['get_forum'].format(7))
    data = r.json()

    topic_ids = [k for k in data['result']]
    search_params = {'by': 'topic_id', 'val': ','.join(topic_ids)}
    r = requests.get(ENDPOINTS['get_peer_stats'], params=search_params)
    topics = r.json()

    assert len(topics['result']) == len(data['result'])


def test_get_tor_hash():
    """ Test checks we can get hash by torrent's id. """

    search_params = {'by': 'topic_id', 'val': '5172825'}
    r = requests.get(ENDPOINTS['get_tor_hash'], params=search_params)
    data = r.json()

    torrent = {'5172825': 'CC3045C6FE4D1B54D72099EF8B65102B4A8CD564'}

    assert data['result'] == torrent


def test_get_topic_id():
    """ Test checks we can get topic id by it's hash. """

    search_params = {'by': 'hash',
                     'val': 'CC3045C6FE4D1B54D72099EF8B65102B4A8CD564'}
    r = requests.get(ENDPOINTS['get_topic_id'], params=search_params)
    data = r.json()

    torrent = {'CC3045C6FE4D1B54D72099EF8B65102B4A8CD564': 5172825}

    assert data['result'] == torrent


def 
