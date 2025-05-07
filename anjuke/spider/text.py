from config import base_url, save_path
from parser import parse_listing_page
from requester import fetch_url
from save import save_to_csv

# 只抓取固定页数进行测试
MAX_PAGES = 3  # 只抓取前3页进行测试


def run_test():
    page = 1  # 从第一页开始
    while page <= MAX_PAGES:
        url = base_url.format(page=page)
        print(f"正在抓取第 {page} 页: {url}")

        # 获取页面 HTML
        html = fetch_url(url)
        if not html:
            print(f" 无法抓取第 {page} 页，跳过")
            page += 1
            continue

        # 解析页面
        listings = parse_listing_page(html)
        if not listings:
            print(" 没有找到任何房源，停止爬取")
            break

        # 保存解析数据到 CSV
        save_to_csv(listings, save_path)
        print(f"第 {page} 页抓取并保存成功，共 {len(listings)} 条房源信息")

        # 跳到下一页
        page += 1


if __name__ == "__main__":
    run_test()
