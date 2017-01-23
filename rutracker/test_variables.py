MAX_LIMIT = 100
HOST = 'http://api.rutracker.org/v1/{0}'
ENDPOINTS = {
    'test_error_response': HOST.format('dbg/test_error_response'),
    'cat_forum_tree': HOST.format('static/cat_forum_tree'),
    'get_forum': HOST.format('static/pvc/f/{0}'),
    'get_limit': HOST.format('get_limit'),
    'get_tor_status_titles': HOST.format('get_tor_status_titles'),
    'get_forum_name': HOST.format('get_forum_name'),
    'get_forum_data': HOST.format('get_forum_data'),
    'get_user_name': HOST.format('get_user_name'),
    'get_peer_stats': HOST.format('get_peer_stats'),
    'get_user_torrents': HOST.format('get_user_torrents'),
    'get_tor_hash': HOST.format('get_tor_hash'),
    'get_topic_id': HOST.format('get_topic_id'),
    'get_tor_topic_data': HOST.format('get_tor_topic_data'),
}
