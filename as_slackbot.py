#!/usr/bin/python
#
# Script to send a message "as slackbot"
#
# We change our display name to slackbot, then send the message, then change it
# back and delete the message, so they get a desktop notification from slackbot
# but can't find it.
#
# Credit for the idea to @xymostech, and to @nelhage for the greek letter
# omicron trick.
#
# Usage: ./as_slackbot.py '#channel-name' 'message'

import sys
import time

import util


@util.memo
def get_id():
    return 'U09K4JYJE'
    # for some reason this isn't supported for API tester tokens?
    return util.call_api('users.identity')['user']['id']


def change_username(username):
    util.call_api('users.profile.set', {
        'user': get_id(),
        'name': 'display_name',
        'value': username,
    })


def send_as_slackbot(channel_name, text):
    old_username = util.call_api('users.profile.get', {
        'user': get_id(),
    })['profile']['display_name']
    change_username(u'slackb\u03bft')
    resp = util.send_as_user(channel_name, text)
    time.sleep(0.3)
    change_username(old_username)
    util.call_api('chat.delete', {
        'ts': resp['ts'],
        'channel': resp['channel'],
    })


if __name__ == '__main__':
    send_as_slackbot(*sys.argv[1:])
