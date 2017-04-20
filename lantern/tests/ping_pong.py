# -*- coding: utf-8 -*-

from locust import task, Locust, TaskSet
import thriftpy
from lantern.settings import ROOT_PATH
from lantern.utils import control_throughput, gen_loop_csv_reader
from lantern.client import RpcClient
import os


class PingPong(TaskSet):
    test_file = gen_loop_csv_reader('csv/test_file.csv', '|')  # 每个参数以|分割,可以自己写

    def on_start(self):
        pingpong_thrift = thriftpy.load(os.path.join(ROOT_PATH, "thrift_file/pingpong.thrift"),
                                        module_name="pingpong_thrift")
        self.pingpong_client = RpcClient(pingpong_thrift.PingPong, '127.0.0.1', 6000)

    @task
    def get_ping(self):
        self.test_file.next()  # 每次获取csv一行数据,可以取出放入thrift、http、socket接口中
        self.pingpong_client.ping()


class ApiPingPong(Locust):
    task_set = PingPong
    stop_timeout = None
    min_wait = 0
    max_wait = 0
