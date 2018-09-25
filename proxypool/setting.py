# Redis地址
REDIS_HOST = '127.0.0.1'
# 端口
REDIS_PORT = 6379
# 密码
REDIS_PASSWORD = 'foobared'
# 关键字
REDIS_KEY = 'proxies'

# 代理分数
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10

# 状态码
VALID_STATUS_CODES = [200, 302]

# 代理池最大数量
POOL_UPPER_THRESHOLD = 50000

# 检查周期
TESTER_CYCLE = 5
# 获取周期
GETTER_CYCLE = 5

# 测试网站, 最好抓谁测谁
TEST_URL = 'http://www.baidu.com'

# API
API_HOST = '0.0.0.0'
API_PORT = 5555

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

# 最大批测试量
BATCH_TEST_SIZE = 10

