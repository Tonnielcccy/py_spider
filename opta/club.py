# _*_ coding: utf-8 _*_
# @Time: 2025/5/17 21:02
# @Email: aocelary@qq.com
# @Author: Tonnie_lcccy
# @File: club.py


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def plot_club_radar(df, teams, features, feature_labels_zh, team_name_map):
    # 筛选数据
    filtered_df = df[df["Team"].isin(teams)]
    if filtered_df.empty:
        raise ValueError(f"未找到球队 {teams} 的数据！")

    # 计算均值并归一化
    club_avg = filtered_df.groupby("Team")[features].mean()
    club_norm = (club_avg - club_avg.min()) / (club_avg.max() - club_avg.min())

    # 构造雷达图角度
    angles = np.linspace(0, 2 * np.pi, len(features), endpoint=False).tolist()
    angles += angles[:1]

    # 绘制雷达图
    fig, ax = plt.subplots(figsize=(8, 6), subplot_kw={'polar': True})
    for team in teams:
        values = club_norm.loc[team].tolist() + club_norm.loc[team].tolist()[:1]
        ax.plot(angles, values, label=team_name_map.get(team, team))
        ax.fill(angles, values, alpha=0.1)

    # 设置标签和样式
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(feature_labels_zh)

    plt.title("俱乐部能力雷达图", pad=20)
    plt.legend(bbox_to_anchor=(1.1, 1.1))
    plt.show()


# 示例调用
if __name__ == "__main__":
    df = pd.read_excel("cleaned_player_data.xlsx")
    features = ['Goals', 'assists', 'tackles', 'interceptions',
                'passes', 'passperc', 'ground_duel_perc', 'aerial_dual_perc']
    feature_labels_zh = ['进球', '助攻', '铲断', '拦截',
                         '传球数', '传球成功率', '地面对抗', '空中对抗']
    teams = ["Liverpool FC"]
    team_name_map = {"Liverpool FC": "利物浦"}

    plot_club_radar(df, teams, features, feature_labels_zh, team_name_map)