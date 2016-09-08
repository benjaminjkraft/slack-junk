import requests

import secrets


class SlackNotOkayException(Exception):
    pass


def call_api(call, data):
    data['token'] = secrets.TOKEN
    res = requests.post('https://slack.com/api/' + call, data).json()
    if res.get('ok'):
        return res
    else:
        raise SlackNotOkayException(res.get('error', str(res)))


def send_as_user(channel, text):
    return call_api('chat.postMessage', {
        'channel': channel,
        'text': text,
        'as_user': 'true',
    })
