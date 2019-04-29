import datetime
import functools
import time

import requests

# Token as secrets.TOKEN = 'xoxp-...', from:
#    https://api.slack.com/custom-integrations/legacy-tokens
import secrets


# Useful KA channel IDs
BOT_TESTING = 'C090KRE5P'
DEPLOYS = 'C096UP7D0'
WHATS_HAPPENING = 'C71A7RFLN'
DEVOPS = 'C8Y4Q1E0J'
DEV_SUPPORT_LOG = 'CB00L3VFZ'
INFRA = 'C3UDL9QN7'


class SlackNotOkayException(Exception):
    pass


def memo(func):
    results = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        assert not kwargs, "kwargs not supported by @memo"
        if args not in results:
            retval = func(*args)
            results[args] = retval
        return results[args]
    return wrapper


def call_api(call, data=None):
    data = data or {}
    data['token'] = secrets.TOKEN
    res = requests.post('https://slack.com/api/' + call, data).json()
    if res.get('ok'):
        return res
    else:
        raise SlackNotOkayException(res.get('error', str(res)))


def send_as_user(channel_name, text, **kwargs):
    params = {
        'channel': channel_name,
        'text': text,
        'as_user': 'true',
    }
    params.update(kwargs)
    return call_api('chat.postMessage', params)


def channel_id(channel_name):
    channels = call_api('channels.list')
    for channel in channels['channels']:
        if '#' + channel['name'] == channel_name:
            return channel['id']


def channel_history(channel_id, max_messages=None, latest=None, oldest=0):
    if isinstance(oldest, datetime.timedelta):
        oldest = datetime.datetime.now() - oldest
    if isinstance(oldest, datetime.datetime):
        oldest = time.mktime(oldest.timetuple())
    if not latest:
        latest = datetime.datetime.now()
    if isinstance(latest, datetime.timedelta):
        latest = datetime.datetime.now() - latest
    if isinstance(latest, datetime.datetime):
        latest = time.mktime(latest.timetuple())
    messages = []
    while max_messages is None or max_messages > 0:
        resp = call_api('channels.history', {
            'channel': channel_id,
            'count': 1000 if max_messages is None else min(max_messages, 1000),
            'oldest': oldest,
            'latest': latest,
        })
        messages.extend(resp['messages'])
        if not resp.get('has_more'):
            break
        if max_messages is not None:
            max_messages -= len(resp['messages'])
        latest = resp['messages'][-1]['ts']

    return messages
