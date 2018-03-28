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


def _version_to_dt(version):
    return datetime.datetime.strptime(version[:11], '%y%m%d-%H%M')


def _week(date):
    return date - datetime.timedelta(date.weekday())


def _weekday(date):
    return (date.weekday(), date.strftime('%A'))


def _print(desc, n, tot=None, graph=False):
    print "%s:" % desc,
    print str(n).rjust(20 - len(desc)),
    if tot:
        print ("(%.1f%%)" % (n * 100./tot)).rjust(7),
    if graph:
        print "#" * n,
    print


def _counts(iterable):
    return sorted(collections.Counter(iterable).items())


def main():
    versions = versions_set_as_default()
    dts = map(_version_to_dt, versions)
    dates = [dt.date() for dt in dts]
    tot = len(versions)

    print "Week of:"
    for day, n in _counts(map(_week, dates)):
        _print("  %s" % day.strftime('%Y-%m-%d'), n, graph=True)
    print

    print "Weekdays:"
    for (_, day_name), n in _counts(map(_weekday, dates)):
        _print("  %s" % day_name, n, tot)
    print

    print "Hour (PDT, start time):"
    hours = [dt.strftime('%H:00') for dt in dts]
    for hour, n in _counts(hours):
        _print("  %s" % hour, n, graph=True)
    print

    print "Deploys/weekday:"
    # TODO(benkraft): Exclude holidays
    weekday_counts = collections.Counter(n for day, n in _counts(dates)
                                         if day.weekday() <= 4)
    min_count = min(weekday_counts)
    max_count = max(weekday_counts)
    for i in xrange(min_count, max_count + 1):
        _print("  %2d deploys" % i, weekday_counts[i], graph=True)

    print
    _print("Total", tot)


if __name__ == '__main__':
    main()
