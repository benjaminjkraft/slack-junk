import random
import sys

sys.path.insert(0, 'lib')

import webapp2
import requests   # noqa: unused import
import requests_toolbelt.adapters.appengine

requests_toolbelt.adapters.appengine.monkeypatch()

import util


USER = '@benkraft'


def _get_messages():
    messages_with_weights = []
    with open('messages.txt') as f:
        for line in f:
            weight, msg = line.split(',', 1)
            weight = float(weight)
            messages_with_weights.append([weight, msg])
    return messages_with_weights


def _choose_from(l):
    total_weight = 0
    for weight, _ in l:
        total_weight += weight
    for item in l:
        item[0] = item[0] / total_weight
    rand = random.random()
    for item in l:
        if rand < item[0]:
            return item[1]
        else:
            rand -= item[0]
    assert False, "something broke %s" % l


def _send_message():
    return util.call_api('chat.postMessage', {
        'channel': USER,
        'text': _choose_from(_get_messages()),
    })


class Send(webapp2.RequestHandler):
    def get(self):
        """Invoked by cron."""
        _send_message()


app = webapp2.WSGIApplication([
    ('/send', Send),
])
