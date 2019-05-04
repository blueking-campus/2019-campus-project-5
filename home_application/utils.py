# -*- coding: utf-8 -*-
import json
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
