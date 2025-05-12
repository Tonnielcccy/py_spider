import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def plot_layout_pie(df, save_path=None):
    """
    根据房屋户型统计数量并绘制饼图

    """
    layout_counts = df['layout'].value_counts().nlargest(6)  # 只显示前6个常见户型，其余可合并为“其他”

    others = df['layout'].value_counts()[6:].sum()
    if others > 0:
        layout_counts['其他'] = others

    # 绘制饼图
    plt.figure(figsize=(8, 6))
    layout_counts.plot.pie(autopct='%1.1f%%', startangle=140, counterclock=False)
    plt.title('房屋户型分布')
    plt.ylabel('')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
        print(f"散点图已保存至：{save_path}")
    plt.show()


def plot_area_vs_price(df, save_path=None):
    """
    绘制房屋面积与租金的散点图。

    """
    # 清洗数据
    df = df.copy()
    df['area'] = df['area'].astype(str).str.extract(r'(\d+\.?\d*)').astype(float)
    df['price'] = df['price'].astype(str).str.extract(r'(\d+\.?\d*)').astype(float)

    # 绘制散点图
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='area', y='price', alpha=0.6, edgecolor='k')
    sns.regplot(data=df, x='area', y='price', scatter=False, color='red', label='拟合线')

    plt.title('房屋面积与租金的关系')
    plt.xlabel('面积（平方米）')
    plt.ylabel('租金（元/月）')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
        print(f"散点图已保存至：{save_path}")
    plt.show()


if __name__ == "__main__":
    df1 = pd.read_csv('anjuke/output/cs_coordinates.csv')
    plot_layout_pie(df1, save_path="anjuke/output/长沙市户型饼图.png")
    plot_area_vs_price(df1, save_path="anjuke/output/长沙市面积租金散点图.png")

    df2 = pd.read_csv('anjuke/output/wh_coordinates.csv')
    plot_layout_pie(df2, save_path="anjuke/output/武汉市户型饼图.png")
    plot_area_vs_price(df2, save_path="anjuke/output/武汉市面积租金散点图.png")