import csv
import json


def csv_files(file_path,desc_path):
    with open("{}".format(file_path), "r", encoding="utf-8") as file:
        content = json.load(file)
        keys = content[0].keys()
        values = [i.values() for i in content]

    with open("{}".format(desc_path), "w", encoding="utf-8") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(keys)
        csv_writer.writerows(values)
