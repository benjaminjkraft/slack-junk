#!/usr/bin/env python
#
# Script to generate animated slack messages
#
# Credit for the idea goes to @mroth.
#
# Usage: ./slackimate.py '#channel-name' 'frame-1' 'frame-2' 'frame-3' ...
# (ctrl-C to end)
# If `--delete` is an argument, the message will be deleted on exit.
#
# alternately:
# >>> import slackimate
# >>> do_animation('#channel-name', frames)  # frames is any iterable

import itertools
import time
import requests
import sys

# Token from https://api.slack.com/web, put as secrets.TOKEN = 'xoxp-...'
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


def do_animation(channel, frames, delay=1, delete=False):
    frames = itertools.cycle(frames)
    resp = call_api('chat.postMessage', {
        'channel': channel,
        'text': next(frames),
        'as_user': 'true',
    })
    ts = resp['ts']
    channel = resp['channel']
    try:
        for frame in frames:
            time.sleep(delay)
            resp = call_api('chat.update', {
                'ts': ts,
                'channel': channel,
                'text': frame,
            })
    finally:
        if delete:
            call_api('chat.delete', {
                'ts': ts,
                'channel': channel,
            })


def main():
    if '--delete' in sys.argv:
        delete = True
        sys.argv.remove('--delete')
    else:
        delete = False
    sys.exit(do_animation(sys.argv[1], sys.argv[2:], delete=delete))

if __name__ == '__main__':
    main()
