import scrapy
import csv
from datetime import datetime
from scrapy.http import Request
from gold.items import SgeItem  # 导入items中的SgeItem类


class SgeSpider(scrapy.Spider):
    name = "fail_sge"
    allowed_domains = ["www.sge.com.cn"]  # 限制爬取的域名

    def __init__(self, url_file='failed_urls.txt', max_retries=3, **kwargs):
        super().__init__(**kwargs)
        self.max_retries = int(max_retries)  # 最大重试次数
        self.failed_urls = []  # 初始失败的 URL 列表
        self.url_file = url_file  # 失败 URL 文件
        # CSV 文件名放到 spider 属性中，pipeline 会使用
        self.filename = f'recrawled_data_{datetime.now().strftime("%Y%m%d")}.csv'  # 保存结果到 CSV 文件
        # 设置表头字段
        self.csv_fields = ['date', 'hy', 'kpj', 'zgj', 'zdj', 'spj', 'zd', 'jqpjj', 'cjl', 'cjje', 'url']

    # 定义爬虫的起始请求
    def start_requests(self):
        # 读取 URL 文件
        with open(self.url_file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
        # 写入日志
        self.logger.info(f"加载到 {len(urls)} 个 URL，开始爬取")
        # 遍历 URL 列表，发送请求
        for url in urls:
            yield Request(url, callback=self.parse_detail, meta={'retries': 0})

    # 从多个方法中选择合适的选择器,找到适合爬取页面的选择器
    def try_selectors(self, row, selectors):
        for sel in selectors:
            text = row.css(sel).get()
            if text and text.strip():
                return text.strip()
        return ''

    # 定义解析函数
    def parse_detail(self, response):
        # 初始失败请求次数,以及记录次数
        retries = response.meta.get('retries', 0)

        # 日期选择器
        date_selectors = [
            'div.title p span::text',
            'div.title p span:nth-of-type(2)::text',
        ]
        # 初始化日期并且遍历选择器,如果在选择器中找到日期,就跳出循环,否则定义为 Unknown
        date = None
        for sel in date_selectors:
            text = response.css(sel).get()
            if text and text.strip() not in ['shanli', 'admin', 'sgeeditor']:
                date = text.strip()
                break
        date = date or 'Unknown'
        # 表格选择器
        table_selectors = [
            'table tbody tr',
            'table tr',
            'div.content table.MsoNormalTable tr',
            'table.MsoNormalTable tr',
            'table.MsoNormalTable.ke-zeroborder tr'
        ]
        # 表格数据选择器
        hy_selectors = ['td:nth-child(1)::text', 'td:nth-child(1) p::text', 'td:nth-child(1) div.MsoNormal span font::text', 'td:nth-child(1) span::text', 'td:nth-child(1) div.MsoNormal font span::text', 'td:nth-child(1) font::text', 'td:nth-child(1) label::text']
        kpj_selectors = ['td:nth-child(2)::text', 'td:nth-child(2) p::text', 'td:nth-child(2) div.MsoNormal span font::text', 'td:nth-child(2) span::text', 'td:nth-child(2) div.MsoNormal font span::text', 'td:nth-child(2) font::text', 'td:nth-child(2) label::text']
        zgj_selectors = ['td:nth-child(3)::text', 'td:nth-child(3) p::text', 'td:nth-child(3) div.MsoNormal span font::text', 'td:nth-child(3) span::text', 'td:nth-child(3) div.MsoNormal font span::text', 'td:nth-child(3) font::text', 'td:nth-child(3) label::text']
        zdj_selectors = ['td:nth-child(4)::text', 'td:nth-child(4) p::text', 'td:nth-child(4) div.MsoNormal span font::text', 'td:nth-child(4) span::text', 'td:nth-child(4) div.MsoNormal font span::text', 'td:nth-child(4) font::text', 'td:nth-child(4) label::text']
        spj_selectors = ['td:nth-child(5)::text', 'td:nth-child(5) p::text', 'td:nth-child(5) div.MsoNormal span font::text', 'td:nth-child(5) span::text', 'td:nth-child(5) div.MsoNormal font span::text', 'td:nth-child(5) font::text', 'td:nth-child(5) label::text']
        zd_selectors = ['td:nth-child(6)::text', 'td:nth-child(6) p::text', 'td:nth-child(6) div.MsoNormal span font::text', 'td:nth-child(6) span::text', 'td:nth-child(6) div.MsoNormal font span::text', 'td:nth-child(6) font::text', 'td:nth-child(6) label::text']
        jqpjj_selectors = ['td:nth-child(7)::text', 'td:nth-child(7) p::text', 'td:nth-child(7) div.MsoNormal span font::text', 'td:nth-child(7) span::text', 'td:nth-child(7) div.MsoNormal font span::text', 'td:nth-child(7) font::text', 'td:nth-child(7) label::text']
        cjl_selectors = ['td:nth-child(8)::text', 'td:nth-child(8) p::text', 'td:nth-child(8) div.MsoNormal span font::text', 'td:nth-child(8) span::text', 'td:nth-child(8) div.MsoNormal font span::text', 'td:nth-child(8) font::text', 'td:nth-child(8) label::text']
        cjje_selectors = ['td:nth-child(9)::text', 'td:nth-child(9) p::text', 'td:nth-child(9) div.MsoNormal span font::text', 'td:nth-child(9) span::text', 'td:nth-child(9) div.MsoNormal font span::text', 'td:nth-child(9) font::text', 'td:nth-child(9) label::text']

        # 初始found为 False,用于判断是否找到表格
        found = False
        for table_sel in table_selectors:
            rows = response.css(table_sel)
            if not rows:
                continue
            # 初始化数据行列表,调用 try_selectors 方法提取数据 并且实时存储到SgeItem中
            data_rows = []
            for row in rows:
                # 如果hy为空,则跳过
                hy = self.try_selectors(row, hy_selectors)
                if not hy:
                    continue
                item = SgeItem()
                item['date'] = date
                item['hy'] = hy
                item['kpj'] = self.try_selectors(row, kpj_selectors)
                item['zgj'] = self.try_selectors(row, zgj_selectors)
                item['zdj'] = self.try_selectors(row, zdj_selectors)
                item['spj'] = self.try_selectors(row, spj_selectors)
                item['zd'] = self.try_selectors(row, zd_selectors)
                item['jqpjj'] = self.try_selectors(row, jqpjj_selectors)
                item['cjl'] = self.try_selectors(row, cjl_selectors)
                item['cjje'] = self.try_selectors(row, cjje_selectors)
                item['url'] = response.url
                data_rows.append(item)
            # 如果data_rows不为空,则打印日志并且返回数据 并且中断表格数据循环
            if data_rows:
                self.logger.info(f"使用选择器 {table_sel} 提取到 {len(data_rows)} 条数据")
                for it in data_rows:
                    yield it
                found = True
                break

        # 如果found依旧为 False,则说明没有找到表格数据,打印日志并且重试
        if not found:
            if retries < self.max_retries:
                self.logger.warning(f"[{response.url}] 解析失败，重试 {retries + 1}/{self.max_retries}")
                yield Request(
                    response.url,
                    callback=self.parse_detail,
                    meta={'retries': retries + 1},
                    dont_filter=True
                )
            # 超过最大重试次数,则打印日志并且保存失败的 URL
            else:
                self.logger.error(f"[{response.url}] 达到最大重试次数，放弃")
                self.failed_urls.append(response.url)

    # 关闭爬虫 并且保存失败的 URL 同时打印日志
    def closed(self, reason):
        if self.failed_urls:
            path = 'failed_urls2.txt'
            with open(path, 'w', encoding='utf-8') as f:
                for url in self.failed_urls:
                    f.write(url + '\n')
            self.logger.info(f"保存 {len(self.failed_urls)} 个失败 URL 到 {path}")
