#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import pytest
import requests

from test_variables import ENDPOINTS, MAX_LIMIT


@pytest.mark.sanity
def test_check_error_response():
    """ Test checks default error code 503. """

    r = requests.get(ENDPOINTS['test_error_response'])

    assert r.status_code == 503


@pytest.mark.sanity
def test_check_get_forums_tree_cat():
    """ Test checks that all categories are presented
        in the list of forums.
    """

    r = requests.get(ENDPOINTS['cat_forum_tree'])
    data = r.json()
    cat_list = data['result']

    # check that we have the same categories in the list of
    # categories and in the result tree:
    missed_categories = [c for c in cat_list['c'] if c not in cat_list['tree']]

    assert missed_categories == []


@pytest.mark.sanity
def test_check_get_forums_tree_cat_count():
    """ Test checks count of categories in the list of
        categories and the full list of forums.
    """

    r = requests.get(ENDPOINTS['cat_forum_tree'])
    data = r.json()

    # check that we have the same amount of categories in the list
    # of categories and in the result tree:
    cat_count = len(data['result']['c'])
    cat_tree_count = len(data['result']['tree'])

    assert cat_count == cat_tree_count 


@pytest.mark.sanity
def test_check_get_forums_tree_forums():
    """ Test checks that all forums are presented
        in the list of forums.
    """

    r = requests.get(ENDPOINTS['cat_forum_tree'])
    data = r.json()
    forums = data['result']['f']
    data_tree = data['result']['tree']
    missed_forums = []

    # check that we have the same forums in the list of
    # forums and in the result tree:
    for category in data_tree:
        for forum in data_tree[category]:
            for subforum in data_tree[category][forum]:
                if str(subforum) not in forums:
                    missed_forums.append(str(subforum))

    assert missed_forums == []


@pytest.mark.sanity
def test_check_get_forums_tree_forums_count():
    """ Test checks count of forums in the list of
        forums and the full list of forums.
    """

    r = requests.get(ENDPOINTS['cat_forum_tree'])
    data = r.json()
    forums_count = len(data['result']['f'])
    data_tree = data['result']['tree']
    tree_forums_count = 0

    # calculate the count of forums in the result tree:
    for category in data_tree:
        tree_forums_count += len(data_tree[category])
        for forum in data_tree[category]:
            tree_forums_count += len(data_tree[category][forum])

    assert forums_count == tree_forums_count


@pytest.mark.sanity
def test_check_get_each_forum():
    """ Test checks that we can get forum by it's id. """

    r = requests.get(ENDPOINTS['get_forum'].format(7))
    data = r.json()

    assert len(data['result']) > 0


@pytest.mark.sanity
def test_check_get_each_forum_fields():
    """ Test checks that we can get forum info by it's id. """

    expected_keys = ['result', 'total_size_bytes', 'format',
                     'update_time', 'update_time_humn']

    r = requests.get(ENDPOINTS['get_forum'].format(7))
    data = r.json()

    # check that we have all required keys in the response json:
    missed_keys = [key for key in expected_keys if key not in data]

    assert missed_keys == []


@pytest.mark.sanity
def test_get_limit():
    """ Test checks that we have right limit. """

    r = requests.get(ENDPOINTS['get_limit'])
    data = r.json()

    assert data['result']['limit'] == MAX_LIMIT


@pytest.mark.sanity
def test_get_tor_status_titles():
    """ Test checks the list of available statuses for topics. """

    expected_statuses = {'0': u'не проверено', '1': u'закрыто',
                         '2': u'проверено', '3': u'недооформлено',
                         '4': u'не оформлено', '5': u'повтор',
                         '6': u'закрыто правообладателем', '7': u'поглощено',
                         '8': u'сомнительно', "9": u'проверяется',
                         '10': u'временная', '11': u'премодерация'}

    r = requests.get(ENDPOINTS['get_tor_status_titles'])
    data = r.json()

    assert data['result'] == expected_statuses


@pytest.mark.sanity
def test_get_forum_name():
    """ Test checks that we can get name of the forum by it's id. """

    forum_id = '7'
    expected_name = u'Зарубежное кино'

    search_params = {'by': 'forum_id', 'val': forum_id}
    r = requests.get(ENDPOINTS['get_forum_name'], params=search_params)
    data = r.json()

    assert data['result'][forum_id] == expected_name


@pytest.mark.sanity
def test_get_forum_name_for_many_forums():
    """ Test checks that we can get name of the forums by their ids. """

    # get full list of forums:
    r = requests.get(ENDPOINTS['cat_forum_tree'])
    data = r.json()
    all_forums = data['result']['f']

    # get first MAX_LIMIT elements from the list of forums:
    forums = {k: all_forums[k] for k in all_forums.keys()[:MAX_LIMIT]}

    # get information about selected MAX_LIMIT forums:
    search_params = {'by': 'forum_id', 'val': ','.join(forums.keys())}
    r = requests.get(ENDPOINTS['get_forum_name'], params=search_params)
    data = r.json()

    assert data['result'] == forums


@pytest.mark.sanity
def test_get_forum_data():
    """ Test checks that we can get forum's data by it's id. """

    furum_id = '7'
    expected_data = {'forum_name': u'Зарубежное кино',
                     'parent_id': 0}

    search_params = {'by': 'forum_id', 'val': furum_id}
    r = requests.get(ENDPOINTS['get_forum_data'], params=search_params)
    data = r.json()

    assert data['result'][furum_id] == expected_data


@pytest.mark.sanity
def test_get_forum_data_for_many_forums():
    """ Test checks that we can get forum's data by ids. """

    r = requests.get(ENDPOINTS['cat_forum_tree'])
    data = r.json()
    data_tree = data['result']['tree']

    res = dict()
    ids_list = list()

    # get dict with subforums and their parents:
    for category in data_tree:
        for forum in data_tree[category]:
            for subforum in data_tree[category][forum]:
                res[str(subforum)] = int(forum)
                ids_list.append(str(subforum))

    ids_string = ','.join(ids_list[:MAX_LIMIT])

    # get info about names of subforums:
    search_params = {'by': 'forum_id', 'val': ids_string}
    r = requests.get(ENDPOINTS['get_forum_name'], params=search_params)
    data = r.json()

    # generate dict for verification:
    forums_data = dict()
    for forum_id, forum_name in data['result'].iteritems():
        forums_data[str(forum_id)] = {'forum_name': forum_name,
                                      'parent_id': res[str(forum_id)]}

    # get detailed info about MAX_LIMIT forums:
    search_params = {'by': 'forum_id', 'val': ids_string}
    r = requests.get(ENDPOINTS['get_forum_data'], params=search_params)
    data = r.json()

    assert data['result'] == forums_data


@pytest.mark.sanity
def test_get_user_name():
    """ Test checks that we can get names of users by their ids. """

    expected_data = {'2': 'admin',
                     '676767': 'figley',
                     '25856984': 'do31415926'}

    search_params = {'by': 'user_id', 'val': ','.join(expected_data.keys())}
    r = requests.get(ENDPOINTS['get_user_name'], params=search_params)
    data = r.json()

    assert data['result'] == expected_data


@pytest.mark.sanity
def test_get_user_torrents():
    """ Test checks that we can get torrents which were created
        by some user.
    """

    user_id = '6477978'

    search_params = {'by': 'user_id', 'val': user_id}
    r = requests.get(ENDPOINTS['get_user_torrents'], params=search_params)
    data = r.json()

    assert len(data['result'][user_id]) > 0


@pytest.mark.sanity
def test_get_topic_data_by_id():
    """ Test checks that we can get topic data by it's id. """

    r = requests.get(ENDPOINTS['get_forum'].format(7))
    data = r.json()
    topic_ids = data['result'].keys()

    search_params = {'by': 'topic_id', 'val': ','.join(topic_ids)}
    r = requests.get(ENDPOINTS['get_peer_stats'], params=search_params)
    topics = r.json()

    # check that we got information about all required topics:
    missed_ids = [i for i in topic_ids if i not in topics['result']]

    assert missed_ids == []


@pytest.mark.sanity
def test_get_tor_hash():
    """ Test checks that we can get hash by torrent's id. """

    torrent = {'5172825': 'CC3045C6FE4D1B54D72099EF8B65102B4A8CD564'}

    search_params = {'by': 'topic_id', 'val': ','.join(torrent.keys())}
    r = requests.get(ENDPOINTS['get_tor_hash'], params=search_params)
    data = r.json()

    assert data['result'] == torrent


@pytest.mark.sanity
def test_get_tor_hash_for_many_torrents():
    """ Test checks that we can get torrents hash by their ids. """

    # user with MAX_LIMIT+ uploaded torrents:
    user_id = '715325'

    # get list of torrents by user_id:
    search_params = {'by': 'user_id', 'val': user_id}
    r = requests.get(ENDPOINTS['get_user_torrents'], params=search_params)
    data = r.json()

    torrents_ids = map(str, data['result'][user_id][:MAX_LIMIT])

    # get hashes for MAX_LIMIT different torrents:
    search_params = {'by': 'topic_id', 'val': ','.join(torrents_ids)}
    r = requests.get(ENDPOINTS['get_tor_hash'], params=search_params)
    data = r.json()

    # check that we got infomration about all required torrents:
    missed_torrents = [t for t in data['result'] if t not in torrents_ids]

    assert missed_torrents == []


@pytest.mark.sanity
def test_get_topic_id():
    """ Test checks that we can get topic id by it's hash. """

    torrent = {'CC3045C6FE4D1B54D72099EF8B65102B4A8CD564': 5172825}

    search_params = {'by': 'hash', 'val': ','.join(torrent.keys())}
    r = requests.get(ENDPOINTS['get_topic_id'], params=search_params)
    data = r.json()

    assert data['result'] == torrent


@pytest.mark.sanity
def test_get_topic_id_for_many_torrents():
    """ Test checks that we can get topics ids by their hashes. """

    # user with MAX_LIMIT+ uploaded torrents:
    user_id = '715325'

    # get list of torrents by user_id:
    search_params = {'by': 'user_id', 'val': user_id}
    r = requests.get(ENDPOINTS['get_user_torrents'], params=search_params)
    data = r.json()

    torrents_ids = map(str, data['result'][user_id][:MAX_LIMIT])

    # get hashes for MAX_LIMIT different torrents:
    search_params = {'by': 'topic_id', 'val': ','.join(torrents_ids)}
    r = requests.get(ENDPOINTS['get_tor_hash'], params=search_params)
    data = r.json()

    # generate data for validation:
    expected_data = {v: int(k) for k, v in data['result'].iteritems()}

    # get ids for MAX_LIMIT different torrents by their hashes:
    search_params = {'by': 'hash', 'val': ','.join(expected_data.keys())}
    r = requests.get(ENDPOINTS['get_topic_id'], params=search_params)
    data = r.json()

    assert data['result'] == expected_data


@pytest.mark.sanity
def test_get_topic_detailed_info():
    """ Test checks that we can get detailed information about
        topic by it's id.
    """

    tor_id = '2142'
    expected_keys = ['info_hash', 'forum_id', 'poster_id', 'size', 'reg_time',
                     'tor_status', 'seeders', 'topic_title',
                     'seeder_last_seen']

    # get torrent data:
    search_params = {'by': 'topic_id', 'val': tor_id}
    r = requests.get(ENDPOINTS['get_tor_topic_data'], params=search_params)
    data = r.json()

    # check that we have all required keys in the response json:
    missed_keys = [k for k in expected_keys if k not in data['result'][tor_id]]

    assert missed_keys == []


@pytest.mark.sanity
def test_get_topic_detailed_info_for_many_torrents():
    """ Test checks that we can get detailed information about
        topics by their ids.
    """

    # user with MAX_LIMIT+ uploaded torrents:
    user_id = '715325'

    # get list of torrents by user_id:
    search_params = {'by': 'user_id', 'val': user_id}
    r = requests.get(ENDPOINTS['get_user_torrents'], params=search_params)
    data = r.json()

    torrents_ids = map(str, data['result'][user_id][:MAX_LIMIT])

    # get information about MAX_LIMIT torrents by their ids:
    search_params = {'by': 'topic_id', 'val': ','.join(torrents_ids)}
    r = requests.get(ENDPOINTS['get_tor_topic_data'], params=search_params)
    data = r.json()

    # check that we have all required torrents in the response json:
    missed_torrents = [t for t in torrents_ids if t not in data['result']]

    assert missed_torrents == []
