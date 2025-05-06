import random
import time

import requests

from config import headers


def fetch_url(url, retries=3):
    for _ in range(retries):
        try:
            req_headers = headers()  # 使用 headers() 函数获取请求头
            response = requests.get(url, headers=req_headers, timeout=10)
            if response.status_code == 200:
                time.sleep(random.uniform(1, 3))
                return response.text
        except requests.RequestException:
            time.sleep(random.uniform(2, 5))
    return None
