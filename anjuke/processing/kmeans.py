from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def plot_elbow_method(df, max_k=15, save_path=None):
    df = df.copy()
    df['area'] = df['area'].astype(str).str.extract(r'(\d+\.?\d*)').astype(float)
    df['price'] = df['price'].astype(str).str.extract(r'(\d+\.?\d*)').astype(float)
    df = df.dropna(subset=['area', 'price'])

    features = StandardScaler().fit_transform(df[['area', 'price']])
    inertia = []
    for k in range(1, max_k + 1):
        km = KMeans(n_clusters=k, random_state=0, n_init=10)
        km.fit(features)
        inertia.append(km.inertia_)

    plt.figure(figsize=(8, 5))
    plt.plot(range(1, max_k + 1), inertia, marker='o')
    plt.title('肘部法选择最佳K值')
    plt.xlabel('聚类簇数 K')
    plt.ylabel('簇内误差平方和 (Inertia)')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()


def kmeans_cluster_area_rent(df, n_clusters=3, save_path=None):
    """
    对房源进行KMeans聚类（基于area和price），并绘制聚类结果散点图。

    """
    df = df.copy()
    df['area'] = df['area'].astype(str).str.extract(r'(\d+\.?\d*)').astype(float)
    df['price'] = df['price'].astype(str).str.extract(r'(\d+\.?\d*)').astype(float)
    df = df.dropna(subset=['area', 'price'])

    # 特征标准化
    scaler = StandardScaler()
    features = scaler.fit_transform(df[['area', 'price']])

    # KMeans聚类
    kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init=10)
    df['set'] = kmeans.fit_predict(features)

    # 可视化
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=df['area'], y=df['price'], hue=df['set'], palette='Set2')
    plt.title(f"KMeans聚类结果（簇数={n_clusters}）")
    plt.xlabel("area")
    plt.ylabel("price")
    plt.legend(title="类别")
    plt.grid(True)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
        print(f"KMeans聚类图已保存至：{save_path}")

    plt.show()

    return df[['area', 'price', 'set']]


if __name__ == "__main__":
    df1 = pd.read_csv('anjuke/output/cs_coordinates.csv')
    plot_elbow_method(df1, max_k=15, save_path="anjuke/output/长沙市肘部法.png")
    df1 = kmeans_cluster_area_rent(df1, n_clusters=4, save_path="anjuke/output/长沙市KMeans聚类.png")

    df2 = pd.read_csv('anjuke/output/wh_coordinates.csv')
    plot_elbow_method(df2, max_k=15, save_path="anjuke/output/武汉市肘部法.png")
    df2 = kmeans_cluster_area_rent(df2, n_clusters=4, save_path="anjuke/output/武汉市KMeans聚类.png")
