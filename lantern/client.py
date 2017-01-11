# -*- coding: utf-8 -*-

import time
from locust import events
from thriftpy.rpc import make_client
import thriftpy


class RpcClient(object):
    def __init__(self, service, host, port):
        self.client = make_client(service, host, port)

    def __getattr__(self, rpc_method):
        func = self.client.__getattr__(rpc_method)

        def wrapper(*args, **kwargs):
            result = None
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
            except Exception, e:
                end_time = time.time()
                total_time = int((end_time - start_time) * 1000)
                events.request_failure.fire(request_type="RpcClient",
                                            name=rpc_method,
                                            response_time=total_time,
                                            exception=e)
            else:
                end_time = time.time()
                total_time = int((end_time - start_time) * 1000)
                events.request_success.fire(request_type="RpcClient",
                                            name=rpc_method,
                                            response_time=total_time,
                                            response_length=0)
            return result

        return wrapper
