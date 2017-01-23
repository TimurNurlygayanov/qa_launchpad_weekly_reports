#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from joblib import Parallel, delayed

def check_status_code200(url):
    r = requests.get(url)
    assert r.status_code == 200, "URL: " + url


def test_check_get_each_forum():
    """ Test checks that we can get any forum from the list of forums. """

    r = requests.get('http://api.rutracker.org/v1/static/cat_forum_tree')
    data = r.json()
    forums_titles = data['result']['f']
    errors = []

    categories_without_torrents = [u'Обсуждения, встречи, общение',
                                   u'Новости',
                                   u'Вопросы по форуму и трекеру',
                                   u'ОБХОД БЛОКИРОВОК']
    ignore_forums = [u'F.A.Q.', u'Архив', u'Ремонт и эксплуатация ТС',
                     u'Общение', u'Помощь по разделу']

    forums = []
    categories = data['result']['tree']
    for category in data['result']['tree']:
        if categories[category] not in categories_without_torrents:
            for f in data['result']['tree'][category].keys():
                forum_without_torrents = False
                for title in ignore_forums:
                    if title in forums_titles[f]:
                        forum_without_torrents = True
                if not forum_without_torrents:
                    forums.append(f)
                    for forum in data['result']['tree'][category]:
                        for f in data['result']['tree'][category][forum]:
                            forum_without_torrents = False
                            for title in ignore_forums:
                                if title in forums_titles[str(f)]:
                                    forum_without_torrents = True

                            if not forum_without_torrents:
                                forums.append(f)

    url = 'http://api.rutracker.org/v1/static/pvc/f/{0}'
    Parallel(n_jobs=1000)(delayed(check_status_code200)(url.format(forum)) for forum in forums)
