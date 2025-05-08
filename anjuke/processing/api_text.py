import pandas as pd
import requests
import time

API_KEY = "17970fe625283146a612648145155379"
SIG = "ee480a03699a29f0e795f5fe2f6f23f6"

# 读取CSV文件
df = pd.read_csv("py_spider/anjuke/output/cs_cleaned_location.csv")

# 只处理前5条记录
df_test = df.head(5)


# 定义地理编码函数，返回字符串 "经度,纬度"
def geocode(standard_location, city=None):
    url = "https://restapi.amap.com/v3/geocode/geo"
    params = {
        "address": standard_location,
        "key": API_KEY,
        "sig": SIG,
        "output": "JSON"
    }
    if city:
        params["city"] = city

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        if data['status'] == '1' and data['geocodes']:
            location = data['geocodes'][0]['location']
            return location
        else:
            print(f"地址解析失败: {standard_location}")
            return None
    except Exception as e:
        print(f"请求出错: {e}")
        return None


# 应用函数
df_test.loc[:, 'location'] = df_test['standard_location'].apply(lambda x: geocode(x, city="长沙"))


# 打印结果
print(df_test[['standard_location', 'location']])


