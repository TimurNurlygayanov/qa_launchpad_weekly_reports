#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# TODO: identify the way to properly filter
#       forums without attached torrents,
#       because get_forum method returns 404
#       status code if forum exists but doesn't have
#       attached torrent files

import pytest
import requests
from joblib import Parallel, delayed

from test_variables import ENDPOINTS


IGNORE_FORUMS = [u'f.a.q.', u'faq', u'архив', u'предложения',
                 u'ремонт и эксплуатация tc', u'общени',
                 u'помощь по разделу', u'ищу']


def check_status_code200(url):
    r = requests.get(url)
    assert r.status_code == 200, "URL: " + url


def check_forum_title(title):
    for w in IGNORE_FORUMS:
        if w.lower() in title.lower():
            return False
    return True


@pytest.mark.long
@pytest.mark.xfail(run=False)
def test_check_get_each_forum():
    """ Test checks that we can get any forum from the list of forums. """

    # get list of all forums:
    r = requests.get(ENDPOINTS['cat_forum_tree'])
    data = r.json()
    forums_titles = data['result']['f']

    categories_without_torrents = [u'Обсуждения, встречи, общение',
                                   u'Новости',
                                   u'Вопросы по форуму и трекеру',
                                   u'ОБХОД БЛОКИРОВОК']

    forums = []
    categories = data['result']['tree']

    # collect all forums with attached torrents:
    for category in categories:
        if categories[category] not in categories_without_torrents:
            for forum in categories[category].keys():
                if check_forum_title(forums_titles[forum]):
                    forums.append(forum)
                    for subforum in categories[category][forum]:
                        if check_forum_title(forums_titles[str(subforum)]):
                            forums.append(subforum)

    # get every torrent from the list and make sure it exists:
    Parallel(n_jobs=1000)(delayed(check_status_code200)
                          (ENDPOINTS['get_forum'].format(forum))
                          for forum in forums)
