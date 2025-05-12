import pandas as pd
import requests
import time


API_KEY = "api_key"
SIG = "sig"


# 定义地理编码函数（返回"经度,纬度"字符串）
def geocode(address, city=None):
    url = "https://restapi.amap.com/v3/geocode/geo"
    params = {
        "address": address,
        "key": API_KEY,
        "sig": SIG,
        "output": "JSON"
    }
    if city:
        params["city"] = "430100"

    max_retries = 3
    retry_count = 0  # 记录失败次数

    while retry_count < max_retries:
        try:
            # 发送请求
            print(f"正在请求地址: {address}")  # 输出当前请求的地址
            response = requests.get(url, params=params, timeout=15)
            data = response.json()

            if data['status'] == '1' and data['geocodes']:
                location = data['geocodes'][0]['location']
                print(f"地址解析成功: {address} -> {location}")  # 成功时输出解析结果
                time.sleep(1)  # 每次成功请求后等待1秒
                return location
            else:
                print(f"地址解析失败: {address}，错误信息: {data.get('info')}")
                retry_count += 1  # 失败次数加1
                time.sleep(1)  # 失败后等待1秒
        except Exception as e:
            print(f"请求异常: {address} - {str(e)}")
            retry_count += 1  # 异常也计为失败
            time.sleep(1)  # 异常后等待1秒

    print(f"连续 {max_retries} 次失败，跳过该地址: {address}")  # 如果连续失败超过三次，输出并跳过
    return None


# 读取数据
df = pd.read_csv("py_spider/anjuke/output/wh_cleaned_location.csv", encoding='utf-8')

# 执行地理编码
print("开始地理编码转换...")
df['location'] = df['standard_location'].apply(geocode)

# 保存结果
df.to_csv("py_spider/anjuke/output/wh_coordinates.csv", index=False, encoding='utf-8')
print(f"转换完成，成功解析 {df['location'].notnull().sum()}/{len(df)} 条地址")

# 检查是否出现了三次连续失败
if df['location'].isnull().sum() > 0:
    print("出现了无法解析的地址，请检查输出文件的详细信息。")
