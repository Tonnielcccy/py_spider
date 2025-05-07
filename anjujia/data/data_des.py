import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter

# 读取数据
df = pd.read_csv("py_spider/anjujia/output/cs_cleaned.csv")

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

print("租金描述统计：")
print(df["price"].describe())

print("\n 面积描述统计：")
print(df["area"].describe())

print("\n 各户型平均租金：")
print(df.groupby("layout")["price"].mean().sort_values(ascending=False))



#  租金分布图
plt.figure(figsize=(8, 5))
sns.histplot(df["price"], bins=30, kde=True)
plt.title("租金分布直方图")
plt.xlabel("租金（元/月）")
plt.ylabel("房源数量")
plt.tight_layout()
plt.savefig("py_spider/anjujia/output/租金分布直方图.png")
plt.show()

# 户型与租金箱线图
plt.figure(figsize=(10, 6))
sns.boxplot(x="layout", y="price", data=df)
plt.title("不同户型的租金分布")
plt.xlabel("户型")
plt.ylabel("租金（元/月）")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("py_spider/anjujia/output/户型租金箱线图.png")
plt.show()



# 标签词云图
tags_text = ",".join(df["tags"].dropna().astype(str).tolist())

# 使用英文逗号和中文逗号都考虑进来
tags_list = tags_text.replace("，", ",").split(",")
tags_list = [tag.strip() for tag in tags_list if tag.strip()]  # 去除空项和多余空格

# 统计词频
tag_freq = Counter(tags_list)

# 生成词云
wordcloud = WordCloud(font_path="msyh.ttc", background_color="white", width=800, height=400).generate_from_frequencies(tag_freq)

# 显示并保存词云图
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("房源标签词云图")
plt.savefig("py_spider/anjujia/output/房源标签词云图.png")
plt.show()

