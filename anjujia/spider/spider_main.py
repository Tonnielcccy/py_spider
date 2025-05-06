import os

from config import base_url, save_path, checkponit_file, log_path, failed_pages
from logger import get_logger
from parser import parse_listing_page
from requester import fetch_url
from save import save_to_csv, save_failed_page

logger = get_logger(log_path)

MAX_CONSECUTIVE_FAILURES = 5  # 最大连续失败次数


def load_checkpoint():
    if os.path.exists(checkponit_file):
        with open(checkponit_file, "r") as f:
            return int(f.read().strip())
    return 1


def save_checkpoint(page):
    with open(checkponit_file, "w") as f:
        f.write(str(page))


def run():
    page = load_checkpoint()
    consecutive_failures = 0
    logger.info(f"从第 {page} 页开始抓取数据")

    while True:
        url = base_url.format(page=page)
        logger.info(f"正在抓取第 {page} 页：{url}")

        # 开始抓取页面
        html = fetch_url(url)
        if not html:
            logger.warning(f"第 {page} 页抓取失败")
            save_failed_page(page, failed_pages)
            consecutive_failures += 1
            if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                logger.error(f"连续失败超过 {MAX_CONSECUTIVE_FAILURES} 页，程序终止")
                break
            continue

        consecutive_failures = 0

        # 解析页面
        listings = parse_listing_page(html)
        if not listings:
            logger.info("未发现更多房源，抓取结束")
            break

        # 保存数据到 CSV
        save_to_csv(listings, save_path)
        logger.info(f"第 {page} 页数据保存成功")

        # 更新检查点
        save_checkpoint(page)

        # 增加页数
        page += 1

    logger.info("程序运行结束")


if __name__ == "__main__":
    run()
