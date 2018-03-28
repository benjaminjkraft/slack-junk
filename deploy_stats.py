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


def _print(desc, n, tot=None):
    print "%s:" % desc,
    print str(n).rjust(20 - len(desc)),
    if tot:
        print ("(%.1f%%)" % (n * 100./tot)).rjust(7),
    print


def _counts(iterable):
    return sorted(collections.Counter(iterable).items())


def main():
    versions = versions_set_as_default()
    dates = map(_version_to_date, versions)
    tot = len(versions)

    print "Week of:"
    for day, n in _counts(map(_week, dates)):
        _print("  %s" % day.strftime('%Y-%m-%d'), n)
    print

    print "Weekdays:"
    for (_, day_name), n in _counts(map(_weekday, dates)):
        _print("  %s" % day_name, n, tot)
    print

    print "Percentiles (of weekdays):"
    # TODO(benkraft): Exclude holidays
    weekdays_by_count = sorted((n, day) for day, n in _counts(dates)
                               if day.weekday() <= 4)
    n, day = weekdays_by_count[0]
    _print("   min (%s)" % day.strftime('%Y-%m-%d'), n)
    for pctile in (5, 50, 95):
        i = int(round(pctile / 100. * len(weekdays_by_count)))
        n, day = weekdays_by_count[i]
        _print("  %2sth (%s)" % (pctile, day.strftime('%Y-%m-%d')),
               n)
    n, day = weekdays_by_count[-1]
    _print("   max (%s)" % day.strftime('%Y-%m-%d'), n)
    print

    print "Distribution (of weekdays):"
    weekday_counts = collections.Counter(n for day, n in _counts(dates)
                                         if day.weekday() <= 4)
    for i in xrange(min(weekday_counts), max(weekday_counts) + 1):
        print '%3d' % i, '#' * weekday_counts[i]

    print
    _print("Total", tot)


if __name__ == '__main__':
    main()
