import pandas as pd
from sqlalchemy import create_engine


def save_to_database(input_file, output_file):
    df = pd.read_excel(input_file)

    #  创建数据库连接
    engine = create_engine("mysql+pymysql://text:391724@localhost/opta?charset=utf8mb4")

    # 保存到数据库中
    df.to_sql(output_file, engine, if_exists="replace", index=False)

    print("数据已成功写入数据库！")


if __name__ == "__main__":
    input_file1 = "cleaned_player_data.xlsx"
    output_file1 = "player_data"
    save_to_database(input_file1, output_file1)

    input_file2 = "players_attack_data.xlsx"
    output_file2 = "attack_data"
    save_to_database(input_file2, output_file2)

    input_file3 = "players_chanceCreation_data.xlsx"
    output_file3 = "chancecreation_data"
    save_to_database(input_file3, output_file3)

    input_file4 = "players_defending_data.xlsx"
    output_file4 = "defending_data"
    save_to_database(input_file4, output_file4)

    input_file5 = "players_possession_data.xlsx"
    output_file5 = "possession_data"
    save_to_database(input_file5, output_file5)

    input_file6 = "players_passing_data.xlsx"
    output_file6 = "passing_data"
    save_to_database(input_file6, output_file6)