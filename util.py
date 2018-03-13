import functools

import requests

import secrets


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
