import redis
from proxypool.error import PoolEmptyError
from proxypool.setting import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_KEY
from proxypool.setting import MAX_SCORE, MIN_SCORE, INITIAL_SCORE
from random import choice
import re


class RedisClient(object):
    """[summary]
    
    存储模块
    """
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT): # 更新2019-06-16，去掉了参数: password=REDIS_PASSWORD
        """[summary]
        
        初始化
        
        Keyword Arguments:
            host {[type]} -- 地址 (default: {REDIS_HOST})
            port {[type]} -- 端口 (default: {REDIS_PORT})
            password {[type]} -- 密码 (default: {REDIS_PASSWORD})
        """ 
        self.db = redis.StrictRedis(host=host, port=port, decode_responses=True) # 更新2019-06-16，去掉了参数: password=password

    def add(self, proxy, score=INITIAL_SCORE):
        """[summary]
        
        添加代理，设置分数为最高
        
        Arguments:
            proxy {[type]} -- 代理
        
        Keyword Arguments:
            score {[type]} -- 分数 (default: {INITIAL_SCORE})
        """     
        if not re.match('\d+\.\d+\.\d+\.\d+:\d+', proxy):
            print('代理不符合规范: ', proxy, ' 丢弃')
            return
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, score, proxy)

    def random(self):
        """[summary]
        
        随机获取有效的代理，首先尝试获取最高分数代理，如果不存在，则按排名获取
        """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MIN_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    def decrease(self, proxy):
        """[summary]
        
        代理值减一分，分数小于最小值，则代理删除
        
        Arguments:
            proxy {[type]} -- 代理
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理:', proxy, '  当前分数:', score, '减1')
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            print('代理:', proxy, '  当前分数:', score, '移除')
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """[summary]
        
        判断代理是否存在
        
        Arguments:
            proxy {[type]} -- 代理
        """
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        """[summary]
        
        将代理设置为MAX_SCORE

        Arguments:
            proxy {[type]} -- 代理
        """
        print('代理:', proxy, '   可用，设置为:', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def count(self):
        """[summary]
        
        获取数量
        """
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """[summary]
        
        获取全部代理
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def batch(self, start, stop):
        """[summary]
        
        批量获取
        
        Arguments:
            start {[type]} -- 开始索引
            stop {[type]} -- 结束索引
        """
        return self.db.zrevrange(REDIS_KEY, start, stop-1)
        

if __name__ == '__main__':
    conn = RedisClient()
    result = conn.batch(680, 688)
    print(result)