import scrapy
import re
from datetime import datetime
from scrapy.http import Request
from gold.items import SgeItem  # 导入 SgeItem 类

class SgeSpider(scrapy.Spider):
    name = "sge"
    allowed_domains = ["www.sge.com.cn"]
    start_urls = ["https://www.sge.com.cn/sjzx/mrhqsj"]

    def __init__(self, max_pages=None, max_retries=3, url_file='failed_urls.txt', **kwargs):
        super().__init__(**kwargs)
        self.max_pages = int(max_pages) if max_pages else None
        self.max_retries = int(max_retries)
        self.failed_urls = []
        self.url_file = url_file  # 失败 URL 保存地址
        self.filename = f'data_{datetime.now().strftime("%Y%m%d")}.csv'  # 保存结果到 CSV 文件
        # 设置表头字段
        self.csv_fields = ['date', 'hy', 'kpj', 'zgj', 'zdj', 'spj', 'zd', 'jqpjj', 'cjl', 'cjje', 'url']

    def parse(self, response):
        for item in response.css('li.lh45.border_ea_b'):
            links = item.css('a.title::attr(href)').getall()
            for link in links:
                yield response.follow(link, callback=self.parse_detail, meta={'retries': 0})

        # 自动翻页
        next_page_div = response.css("div.btn.border_ea.noLeft_border[onclick*='gotoPage']")
        if next_page_div:
            onclick = next_page_div.attrib.get('onclick')
            if onclick:
                match = re.search(r"gotoPage\('/sjzx/mrhqsj\?p=','(\d+)'\)", onclick)
                if match:
                    current_page = int(match.group(1))
                    if self.max_pages is not None and current_page >= self.max_pages:
                        self.logger.info(f"达到最大页码 {self.max_pages}，停止爬取。")
                        return
                    next_page = f"https://www.sge.com.cn/sjzx/mrhqsj?p={current_page}"
                    yield response.follow(next_page, callback=self.parse, meta={'page': current_page})

    def try_selectors(self, row, selectors):
        for sel in selectors:
            text = row.css(sel).get()
            if text and text.strip():
                return text.strip()
        return ''

    def parse_detail(self, response):
        retries = response.meta.get('retries', 0)

        # 日期选择器
        date_selectors = [
            'div.title p span::text',
            'div.title p span:nth-of-type(2)::text',
        ]
        # 初始化日期
        date = None
        for sel in date_selectors:
            text = response.css(sel).get()
            if text and re.search(r'^[^\u4e00-\u9fff a-zA-Z]+$', text.strip()):
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
        hy_selectors = ['td:nth-child(1)::text', 'td:nth-child(1) p::text', 'td:nth-child(1) div.MsoNormal span font::text', 'td:nth-child(1) span::text', 'td:nth-child(1) div.MsoNormal font span::text']
        kpj_selectors = ['td:nth-child(2)::text', 'td:nth-child(2) p::text', 'td:nth-child(2) div.MsoNormal span font::text', 'td:nth-child(2) span::text', 'td:nth-child(2) div.MsoNormal font span::text']
        zgj_selectors = ['td:nth-child(3)::text', 'td:nth-child(3) p::text', 'td:nth-child(3) div.MsoNormal span font::text', 'td:nth-child(3) span::text', 'td:nth-child(3) div.MsoNormal font span::text']
        zdj_selectors = ['td:nth-child(4)::text', 'td:nth-child(4) p::text', 'td:nth-child(4) div.MsoNormal span font::text', 'td:nth-child(4) span::text', 'td:nth-child(4) div.MsoNormal font span::text']
        spj_selectors = ['td:nth-child(5)::text', 'td:nth-child(5) p::text', 'td:nth-child(5) div.MsoNormal span font::text', 'td:nth-child(5) span::text', 'td:nth-child(5) div.MsoNormal font span::text']
        zd_selectors = ['td:nth-child(6)::text', 'td:nth-child(6) p::text', 'td:nth-child(6) div.MsoNormal span font::text', 'td:nth-child(6) span::text', 'td:nth-child(6) div.MsoNormal font span::text']
        jqpjj_selectors = ['td:nth-child(7)::text', 'td:nth-child(7) p::text', 'td:nth-child(7) div.MsoNormal span font::text', 'td:nth-child(7) span::text', 'td:nth-child(7) div.MsoNormal font span::text']
        cjl_selectors = ['td:nth-child(8)::text', 'td:nth-child(8) p::text', 'td:nth-child(8) div.MsoNormal span font::text', 'td:nth-child(8) span::text', 'td:nth-child(8) div.MsoNormal font span::text']
        cjje_selectors = ['td:nth-child(9)::text', 'td:nth-child(9) p::text', 'td:nth-child(9) div.MsoNormal span font::text', 'td:nth-child(9) span::text', 'td:nth-child(9) div.MsoNormal font span::text']

        found = False
        for table_sel in table_selectors:
            rows = response.css(table_sel)
            if not rows:
                continue
            data_rows = []
            for row in rows:
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
            if data_rows:
                self.logger.info(f"使用选择器 {table_sel} 提取到 {len(data_rows)} 条数据")
                for it in data_rows:
                    yield it
                found = True
                break

        if not found:
            if retries < self.max_retries:
                self.logger.warning(f"[{response.url}] 解析失败，重试 {retries + 1}/{self.max_retries}")
                yield Request(
                    response.url,
                    callback=self.parse_detail,
                    meta={'retries': retries + 1},
                    dont_filter=True
                )
            else:
                self.logger.error(f"[{response.url}] 达到最大重试次数，放弃")
                self.failed_urls.append(response.url)

    def closed(self, reason):
        if self.failed_urls:
            with open(self.url_file, 'w', encoding='utf-8') as f:
                for url in self.failed_urls:
                    f.write(url + '\n')
            self.logger.info(f"保存 {len(self.failed_urls)} 个失败 URL 到 {self.url_file}")