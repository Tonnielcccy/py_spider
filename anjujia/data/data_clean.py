import pandas as pd
# 预设列名
column_names = ["title", "price", "unit", "layout", "area", "floor", "community", "location", "tags"]

# 1. 加载数据，给定列名
def load_data(file_path):
    return pd.read_csv(file_path, names=column_names, header=None)


# 2. 处理缺失值
def handle_missing_data(df):
    # 检查每列缺失值情况
    print("缺失值统计：")
    print(df.isnull().sum())

    # 你可以选择以下方法：
    # a. 删除含有缺失值的行
    # df = df.dropna()

    # b. 用某个值填充缺失值（比如使用列的均值、众数等）
    # df['price'] = df['price'].fillna(df['price'].mean())  # 用均值填充

    # c. 如果缺失值过多且不重要，直接删除列
    # df = df.drop(columns=['some_column_with_many_na'])

    return df


# 3. 格式转换
def convert_data_types(df):
    # 将 'price' 列转换为数字类型
    df['price'] = pd.to_numeric(df['price'], errors='coerce')

    # 如果 'area' 列是字符串，去除单位（如 "m²"），并转化为浮动数字
    df['area'] = df['area'].str.replace('平米', '').astype(float)

    # 处理日期列，如果存在
    # df['date'] = pd.to_datetime(df['date'], errors='coerce')

    return df


# 4. 去重
def remove_duplicates(df):
    print(f"去重前的行数: {len(df)}")
    df = df.drop_duplicates()
    print(f"去重后的行数: {len(df)}")
    return df


# 5. 异常值处理
def handle_outliers(df):
    # 例如，价格不可能为负数
    df = df[df['price'] > 0]

    # 如果面积为0或不合理，也可以过滤掉
    df = df[df['area'] > 0]

    return df


# 6. 文本清洗
def clean_text(df):
    # 去除 'location' 列中的多余空格和特殊字符
    df['location'] = df['location'].str.strip().str.replace(r'[^\w\s]', '', regex=True)

    return df


# 7. 保存清洗后的数据
def save_cleaned_data(df, output_path):
    df.to_csv(output_path, index=False)
    print(f"清洗后的数据已保存到: {output_path}")


# 清洗流程
def clean_data(file_path, output_path):
    df = load_data(file_path)
    df = handle_missing_data(df)
    df = convert_data_types(df)
    df = remove_duplicates(df)
    df = handle_outliers(df)
    df = clean_text(df)
    save_cleaned_data(df, output_path)


# 运行数据清洗流程
input_file = 'output/cs_anjuke_rentals.csv'  # 输入文件路径
output_file = 'output/cs_cleaned.csv'  # 输出文件路径

clean_data(input_file, output_file)
