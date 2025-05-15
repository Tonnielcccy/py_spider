import pandas as pd
from sqlalchemy import create_engine

def save_to_database(input_file, output_file):

    df = pd.read_csv(input_file, encoding="utf-8")

    #  创建数据库连接
    engine = create_engine("mysql+pymysql://text:391724@localhost/anjuke?charset=utf8mb4")

    # 保存到数据库中
    df.to_sql(output_file, engine, if_exists="replace", index=False)

    print("数据已成功写入数据库！")

if __name__ == "__main__":
    input_file1 = "anjuke/output/cs_coordinates.csv"
    output_file1 = "cs_data"
    save_to_database(input_file1, output_file1)

    input_file2 = "anjuke/output/wh_coordinates.csv"
    output_file2 = "wh_data"
    save_to_database(input_file2, output_file2)