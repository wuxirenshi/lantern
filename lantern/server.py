import thriftpy
from thriftpy.rpc import make_server
import os
from lantern.settings import ROOT_PATH

pingpong_thrift = thriftpy.load(os.path.join(ROOT_PATH, "thrift_file/pingpong.thrift"), module_name="pingpong_thrift")


class Dispatcher(object):
    def ping(self):
        return "pong"


server = make_server(pingpong_thrift.PingPong, Dispatcher(), '127.0.0.1', 6000)
server.serve()
