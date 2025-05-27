# _*_ coding: utf-8 _*_
# @Time: 2025/5/25 12:21
# @Email: aocelary@qq.com
# @Author: Tonnie_lcccy
# @File: clean.py


import pandas as pd


# 读取原始 CSV 和重新爬取的 CSV
original_csv = 'data_20250523.csv'
recrawled_csv = 'recrawled_data_20250523.csv'
recrawled_csv1 = 'recrawled_data_20250524.csv'

df_original = pd.read_csv(original_csv)
df_recrawled = pd.read_csv(recrawled_csv)
df_recrawled1 = pd.read_csv(recrawled_csv1)

# 删除原始数据中有问题的行（根据 URL）
df_original = df_original[~df_original['url'].isin(df_recrawled['url'])]
df_original = df_original[~df_original['url'].isin(df_recrawled1['url'])]

# 合并数据
df_final = pd.concat([df_original, df_recrawled, df_recrawled1], ignore_index=True)

# 调试：打印 date 列的唯一值，检查原始数据内容
print("合并后 date 列的唯一值：")
print(df_final['date'].unique())

# 将 date 列转换为标准 datetime 格式，处理无效值
df_final['date'] = pd.to_datetime(df_final['date'], errors='coerce')

# 检查无效日期的行
invalid_dates = df_final[df_final['date'].isna()]
if not invalid_dates.empty:
    print("以下行的日期无效：")
    print(invalid_dates[['url', 'date']])

# 将 date 列格式化为标准字符串格式 %Y-%m-%d
df_final['date'] = df_final['date'].dt.strftime('%Y-%m-%d')

# 按照 date 列进行排序（升序）
df_final = df_final.sort_values(by='date', ascending=True)

# 保存合并后的数据
final_csv = f'cleaned.csv'
df_final.to_csv(final_csv, index=False, encoding='utf-8')
print(f"合并后的数据已保存到 {final_csv}")