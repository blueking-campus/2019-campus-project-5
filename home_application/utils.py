# -*- coding: utf-8 -*-
import json
import time
import datetime


class DateJSONEncoder(json.JSONEncoder):
    """date-json编码"""

    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, o)

def is_vaild_datetime(date):
    """
    判断是否是datetime格式字符串
    date: %Y-%m-%d %H:%M:%S
    """
    try:
        time.strptime(date, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError, err:
        print err
        return False


def is_int(num):
    """判断是否是int格式的字符串"""
    try:
        int(num)
        return True
    except ValueError, err:
        print err
        return False
