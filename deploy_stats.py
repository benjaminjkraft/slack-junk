#!/usr/bin/env python2
import collections
import datetime

import util


START_TIME = datetime.datetime(2018, 1, 1)


def get_messages():
    return util.channel_history(util.WHATS_HAPPENING, oldest=START_TIME)


def _extract_version_set(msg):
    if msg.startswith('Default version set to'):
        return msg.split()[4]
    elif msg.startswith('Default static-content version set to'):
        return msg.split()[5]
    else:
        return None


def versions_set_as_default():
    texts = [message['attachments'][0]['text']
             for message in get_messages()
             if 'attachments' in message]
    versions = filter(None, map(_extract_version_set, texts))
    versions_seen = set()
    unique_versions = []
    for v in versions:
        if v not in versions_seen:
            versions_seen.add(v)
            unique_versions.append(v)
    return unique_versions


def _version_to_date(version):
    return datetime.datetime.strptime(version[:6], '%y%m%d').date()


def _week(date):
    return date - datetime.timedelta(date.weekday())


def _weekday(date):
    return (date.weekday(), date.strftime('%A'))


def _print(desc, n, tot, width=25):
    print "%s:" % desc,
    print str(n).rjust(22 - len(desc)),
    print ("(%.1f%%)" % (n * 100./tot)).rjust(8)


def _counts(iterable):
    return sorted(collections.Counter(iterable).items())


def main():
    versions = versions_set_as_default()
    dates = map(_version_to_date, versions)
    tot = len(versions)
    for day, n in _counts(map(_week, dates)):
        _print("Week of %s" % day.strftime('%Y-%m-%d'), n, tot)
    print
    for (_, day_name), n in _counts(map(_weekday, dates)):
        _print("%s" % day_name, n, tot)
    print
    _print("Total", len(versions), tot)


if __name__ == '__main__':
    main()
