import pandas as pd
import json


def csv_to_json(input_file, output_file):
    """
    将 CSV 文件转换为 JSON 格式
    """

    # 读取CSV数据
    df = pd.read_csv(input_file)

    # 清洗 location 列
    df['location'] = df['location'].astype(str).str.strip()

    #  拆分经纬度列
    df[['lng', 'lat']] = df['location'].str.split(',', expand=True)
    df['lng'] = pd.to_numeric(df['lng'], errors='coerce')
    df['lat'] = pd.to_numeric(df['lat'], errors='coerce')

    # 按 lng, lat 分组，计算平均租金
    df_grouped = df.groupby(['lng', 'lat'], as_index=False)["price"].mean()

    #  构建热力图 JSON 数据结构
    heatmap_data = [
        {"lng": row["lng"], "lat": row["lat"], "count": round(row["price"], 2)}
        for _, row in df_grouped.iterrows()
    ]

    # 输出到 JSON 文件
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(heatmap_data, f, ensure_ascii=False)

    print("已成功生成")


if __name__ == "__main__":
    #长沙市
    input_file = "anjuke/output/cs_coordinates.csv"
    output_file = "cs_data.json"
    csv_to_json(input_file, output_file)

    #武汉市
    input_file1 = "anjuke/output/wh_coordinates.csv"
    output_file1 = "wh_data.json"
    csv_to_json(input_file1, output_file1)