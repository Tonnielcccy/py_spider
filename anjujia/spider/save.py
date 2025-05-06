import csv
import os


def save_to_csv(data, filename):
    file_exists = os.path.isfile(filename)
    fieldnames = ["title", "price", "unit", "layout", "area", "floor", "community", "location", "tags"]

    try:
        with open(filename, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()

            # 转换 tags 为字符串
            for row in data:
                if isinstance(row.get("tags"), list):
                    row["tags"] = ", ".join(row["tags"])
            writer.writerows(data)
    except Exception as e:
        print(f"写入CSV文件失败：{e}")


def save_failed_page(page, filename):
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"{page}\n")
    except Exception as e:
        print(f"写入失败页码时出错：{e}")
