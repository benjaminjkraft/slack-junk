#!/usr/bin/env python
#
# Script to generate my chameleon standup
#
# Usage: ./chameleon_standup.py, then type standup.

import random

import pycountry

import util


DEFAULT_CHANNEL = '#chameleon'
INTRO_LINE = ':snake: *BENKRAFT STANDUP* :snake:'


def get_message_parts():
    message_parts = []
    print INTRO_LINE
    try:
        while True:
            part = raw_input()
            if not part:
                break
            message_parts.append(part)
    except EOFError:
        pass
    return message_parts


def build_full_message(parts):
    countries = random.sample(pycountry.countries, len(parts))
    return '\n'.join([INTRO_LINE] + [
        ':flag-%s: %s' % (country.alpha2, part)
        for (country, part) in zip(countries, parts)])


def main(channel=DEFAULT_CHANNEL):
    util.send_as_user(channel, build_full_message(get_message_parts()))


if __name__ == '__main__':
    main()
