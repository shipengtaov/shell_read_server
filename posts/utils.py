# -*- coding: utf-8 -*-

import datetime


def min_created_at(now=None):
    if now is None:
        now = datetime.datetime.now()
    min_date = now + datetime.timedelta(days=-3)
    return min_date
    return min_date.strftime('%Y-%m-%d %H:%M:%S')
