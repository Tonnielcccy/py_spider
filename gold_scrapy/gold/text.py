import pandas as pd

# 配置路径和条件
csv_path = 'data/data_20250523.csv'
output_path = 'cleaned_data_by_time.csv'
target_value = 'Au99.99'  # 要处理的区域

# 读取数据
df = pd.read_csv(csv_path)

# 获取列名（假设第一列为时间，第二列为区域，第三列为房源名或其他主键）
col_time, col_area = df.columns[0], df.columns[1]

# 将第一列转为 datetime 格式
df[col_time] = pd.to_datetime(df[col_time], errors='coerce')

# 找出目标区域的数据
target_df = df[df[col_area] == target_value]

# 保留该区域中时间最新的一条（假设按某列如房源名去重，保留最新时间）
# 假设第三列是房源名称或唯一标识
col_key = df.columns[2]
target_df_sorted = target_df.sort_values(by=col_time, ascending=False)
target_df_dedup = target_df_sorted.drop_duplicates(subset=col_key, keep='first')

# 非目标区域数据 + 去重后的目标区域数据合并
df_rest = df[df[col_area] != target_value]
df_cleaned = pd.concat([df_rest, target_df_dedup], ignore_index=True)

# 按时间排序（可选）
df_cleaned = df_cleaned.sort_values(by=col_time)

# 保存结果
df_cleaned.to_csv(output_path, index=False)
print(f"已去重并保留最新记录，保存到: {output_path}")
