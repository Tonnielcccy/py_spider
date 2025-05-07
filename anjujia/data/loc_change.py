import pandas as pd

# 替换映射表
replace_dict = {
    # 长沙市
    "芙蓉": "长沙市芙蓉区",
    "天心": "长沙市天心区",
    "岳麓": "长沙市岳麓区",
    "开福": "长沙市开福区",
    "雨花": "长沙市雨花区",
    "望城": "长沙市望城区",
    "长沙县": "长沙市长沙县",
    "星沙": "长沙市星沙",

    # 武汉市
    "江岸": "武汉市江岸区",
    "江汉": "武汉市江汉区",
    "硚口": "武汉市硚口区",
    "汉阳": "武汉市汉阳区",
    "武昌": "武汉市武昌区",
    "青山": "武汉市青山区",
    "洪山": "武汉市洪山区",
    "东西湖": "武汉市东西湖区",
    "汉南": "武汉市汉南区",
    "蔡甸": "武汉市蔡甸区",
    "江夏": "武汉市江夏区",
    "黄陂": "武汉市黄陂区",
    "新洲": "武汉市新洲区",
    "东湖高新": "武汉市东湖高新区",
    "东湖开发区": "武汉市东湖高新区",
    "武汉经济技术开发区": "武汉市经开区"
}


def standardize_location(location_series):
    cleaned = location_series.str.replace(" ", "", regex=False)
    for key, value in replace_dict.items():
        cleaned = cleaned.str.replace(key, value, regex=False)
    return cleaned


def process_file(file_path, output_path):
    df = pd.read_csv(file_path, encoding="utf-8")  # 如有编码问题可换为 encoding="utf-8" 或 errors="ignore"

    if "location" not in df.columns:
        print(f"文件 {file_path} 中未找到 'location' 列")
        return

    df["standard_location"] = standardize_location(df["location"])
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"处理完成：{output_path}")


if __name__ == "__main__":
    # 修改成你自己的文件路径
    changsha_file = "py_spider/anjujia/output/cs_cleaned.csv"
    wuhan_file = "py_spider/anjujia/output/wh_cleaned.csv"

    process_file(changsha_file, "py_spider/anjujia/output/cs_cleaned_location.csv")
    process_file(wuhan_file, "py_spider/anjujia/output/wh_cleaned_location.csv")
