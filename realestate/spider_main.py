import os
from config import base_url, save_path, checkponit_file, log_path, failed_pages
from logger import get_logger
from requester import fetch_url
from parser import parse_listing_page
from save import save_to_csv, save_failed_page

logger = get_logger(log_path)

MAX_CONSECUTIVE_FAILURES = 5

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
    while True:
        url = base_url.format(page=page)
        logger.info(f"Fetching page {page}: {url}")
        html = fetch_url(url)
        if not html:
            logger.warning(f"Failed to fetch page {page}")
            save_failed_page(page, failed_pages)
            consecutive_failures += 1
            if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                logger.error(f"Reached {MAX_CONSECUTIVE_FAILURES} consecutive failures. Terminating.")
                break
            continue
        consecutive_failures = 0
        listings = parse_listing_page(html)
        if not listings:
            logger.info("No more listings found. Stopping.")
            break
        save_to_csv(listings, save_path)
        save_checkpoint(page)
        page += 1

if __name__ == "__main__":
    run()
