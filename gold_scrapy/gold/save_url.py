# _*_ coding: utf-8 _*_
# @Time: 2025/5/23 18:29
# @Email: aocelary@qq.com
# @Author: Tonnie_lcccy
# @File: save_url.py

import pandas as pd

# 读取 CSV 文件
csv_file = 'data/data_20250523.csv'  # 替换为你的 CSV 文件名
df = pd.read_csv(csv_file)

# 筛选出有问题的行
problematic_rows = df[
    df['date'].isin(['shanli', 'admin', 'sgeeditor']) |  # date 错误
    df['hy'].isna() | (df['hy'] == '')  # hy 为空
]

# 提取需要重新爬取的 URL
urls_to_recrawl = problematic_rows['url'].unique().tolist()
print(f"需要重新爬取的 URL 数量: {len(urls_to_recrawl)}")

with open('urls_to_recrawl.txt', 'w', encoding='utf-8') as f:
    for url in urls_to_recrawl:
        f.write(url + '\n')