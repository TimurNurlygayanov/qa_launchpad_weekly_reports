# get horizon pull requests
# retrieve user ids
# get user info
# filter mirantis emails
# compose mirantis pull requests

import json
import multiprocessing
from urllib2 import urlopen

# need to make `pip install futures`
# from concurrent import futures

PROJECT = "openstack/horizon"

project_pull_requests_url_tmpl = "https://review.openstack.org/changes/?q=project:{}"
user_info_url_tmpl = "https://review.openstack.org/accounts/{}"
pull_request_url_tmpl = "https://review.openstack.org/#/c/{}"

project_name = PROJECT.replace('/', '%2F')

def download_json(url):
    opened_url = urlopen(url)
    content = opened_url.read()
    content = ''.join(content.split())

    if content.startswith(")]}'"):
        content = content[4:]  # reject non-json )]}'

    return json.loads(content)

horizon_pull_requests = download_json(project_pull_requests_url_tmpl.format(project_name))
uniq_user_ids = {pr['owner']['_account_id'] for pr in horizon_pull_requests}

pool = multiprocessing.Pool(processes=len(uniq_user_ids))
user_info = pool.map(download_json, map(user_info_url_tmpl.format, uniq_user_ids))

# with futures a bit faster
# with futures.ThreadPoolExecutor(max_workers=len(uniq_user_ids)) as pool:
#     user_info = pool.map(download_json, map(user_info_url_tmpl.format, uniq_user_ids))

mirantis_user_ids = [user['_account_id'] for user in user_info
                     if user.get('email', '').endswith('@mirantis.com')]

mirantis_pull_requests = [pull_request_url_tmpl.format(pr['_number'])
                          for pr in horizon_pull_requests
                          if pr['owner']['_account_id'] in mirantis_user_ids
                          and pr['status'] == 'NEW']

f = open('mirantis_pull_requests.txt', 'w')
f.write('\n'.join(mirantis_pull_requests))
f.close()
