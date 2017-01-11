## Usage
对thrift接口进行压测

启动server
    ``export PYTHONPATH=`pwd` ``
    ``python lantern/server.py``
    
启动压测脚本
    ``export PYTHONPATH=`pwd` ``
    ``locust -f lantern/tests/ping_pong.py``
    
control_throughput可以控制吞吐量
gen_loop_csv_reader解析csv文件