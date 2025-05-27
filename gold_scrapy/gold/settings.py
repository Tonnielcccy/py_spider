# Scrapy settings for gold project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "gold"

SPIDER_MODULES = ["gold.spiders"]
NEWSPIDER_MODULE = "gold.spiders"

ADDONS = {}

DOWNLOADER_MIDDLEWARES = {
    'gold.middlewares.RandomUserAgentMiddleware': 400,
    'gold.middlewares.CustomHeadersMiddleware': 410,
    'gold.middlewares.CustomCookiesMiddleware': 420,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  # 禁用默认 UserAgent 中间件
}
ITEM_PIPELINES = {
     'gold.pipelines.CsvPipeline': 300,
}
DUPEFILTER_CLASS = 'scrapy.dupefilters.RFPDupeFilter'
USER_AGENT = None  # 交给 RandomUserAgentMiddleware 处理
ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 2  # 延迟 2 秒，降低反爬风险
REDIRECT_MAX_TIMES = 10
CONCURRENT_REQUESTS = 8  # 控制并发请求数
LOG_LEVEL = 'INFO'  # 设置日志级别
HTTPCACHE_ENABLED = False  # 临时禁用缓存
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
JOBDIR = 'crawls/sge'
# 日志配置
LOG_FILE = 'spider.log'
LOG_ENCODING = 'utf-8'
CONCURRENT_REQUESTS_PER_DOMAIN = 4
# Configure maximum concurrent requests performed by Scrapy (default: 16)


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "gold (+http://www.yourdomain.com)"

# Obey robots.txt rules


# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "gold.middlewares.GoldSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "gold.middlewares.GoldDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "gold.pipelines.GoldPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"
