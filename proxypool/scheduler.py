import time
from multiprocessing import Process
from proxypool.api import app
from proxypool.getter import Getter
from proxypool.tester import Tester
from proxypool.db import RedisClient
from proxypool.setting import *


class Scheduler():
    def schedule_tester(self, cycle=TESTER_CYCLE):
        """[summary]
        
        定时测试代理
        
        Keyword Arguments:
            cycle {[type]} -- [description] (default: {TESTER_CYCLE})
        """
        tester = Tester()
        while True:
            print('测试器开始运行::')
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        """[summary]
        
        定时获取代理
        
        Keyword Arguments:
            cycle {[type]} -- [description] (default: {GETTER_CYCLE})
        """
        getter = Getter()
        # print(getter.redis.count(getter.redis))
        while True:
            print('开始抓取代理:')
            getter.run()
            time.sleep(cycle)


    def schedule_api(self):
        """[summary]
        
        开启API
        """
        app.run(API_HOST, API_PORT)

    def run(self):
        print('代理池开始运行:')
        # 并行执行
        if TESTER_ENABLED:
            # 新建一个进程
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()

        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()