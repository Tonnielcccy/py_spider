import csv
import os

def save_to_csv(data, filename):
    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price", "detail", "position"])
        if not file_exists:
            writer.writeheader()
        writer.writerows(data)

def save_failed_page(page, filename):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{page}\n")
