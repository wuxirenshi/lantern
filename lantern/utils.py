# -*- coding: utf-8 -*-

import csv
import os
import json
from lantern import settings
import time
import functools


def gen_loop_csv_reader(relative_csv_filename, register=None):
    csv_filename = os.path.join(settings.ROOT_PATH, relative_csv_filename)
    if register:
        csv.register_dialect('vertical', delimiter=register, quoting=csv.QUOTE_NONE)
    with open(csv_filename, "r") as f:
        if register:
            reader = csv.reader(f, dialect='vertical')
        else:
            reader = csv.reader(f)
        rows = [row for row in reader if row]
    length = len(rows)
    index = 0

    while True:
        yield rows[index]
        index += 1
        if index == length:
            index = 0


def control_throughput(throughput, interval_time=None, max_throughput=None):
    def decorated(func):
        num_reqs_per_sec = {}
        first_time = int(time.time())

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cur_time = int(time.time())
            multiple = 1
            if interval_time:
                multiple = int((cur_time - first_time) / interval_time) + 1
                if max_throughput:
                    if throughput * multiple >= max_throughput and num_reqs_per_sec.get(cur_time, 0) >= max_throughput:
                        return
            if num_reqs_per_sec.get(cur_time, 0) >= throughput * multiple:
                return
            num_reqs_per_sec[cur_time] = num_reqs_per_sec.setdefault(cur_time, 0) + 1
            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorated


def transformation(data):
    data_s = [None, True, False]
    if data.strip() == 'None':
        data = None
    elif data.strip() == 'False':
        data = False
    elif data.strip() == 'True':
        data = True
    return data if data in data_s else json.loads(data)


