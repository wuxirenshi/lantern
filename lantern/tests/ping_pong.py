# -*- coding: utf-8 -*-

from locust import task, Locust, TaskSet
import thriftpy
from lantern.settings import ROOT_PATH
from lantern.utils import control_throughput, gen_loop_csv_reader
from lantern.client import RpcClient
import os


class PingPong(TaskSet):
    test_file = gen_loop_csv_reader('csv/test_file.csv', '|')

    def on_start(self):
        pingpong_thrift = thriftpy.load(os.path.join(ROOT_PATH, "thrift_file/pingpong.thrift"),
                                        module_name="pingpong_thrift")
        self.pingpong_client = RpcClient(pingpong_thrift.PingPong, '127.0.0.1', 6000)

    @task
    @control_throughput(100)
    def get_ping(self):
        self.pingpong_client.ping()


class ApiPingPong(Locust):
    task_set = PingPong
    stop_timeout = None
    min_wait = 0
    max_wait = 0
