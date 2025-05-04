import requests
import time
import random
from config import headers

def fetch_url(url, retries=3):
    for _ in range(retries):
        try:
            headers = headers()
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                time.sleep(random.uniform(1, 3))
                return response.text
        except requests.RequestException:
            time.sleep(random.uniform(2, 5))
    return None