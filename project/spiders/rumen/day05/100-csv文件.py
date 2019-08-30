import csv
import json


def f1():
    with open("./files/mycsv.csv", "w", encoding="utf-8") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["sid", "sname", "sage"])
        csv_writer.writerows([[1, "a", 20], [2, "a", 20], [3, "a", 20]])


def f2():
    with open("./files/tecent.json", "r", encoding="utf-8") as file:
        content = json.load(file)
        keys = content[0].keys()
        values = [i.values() for i in content]

    with open("./files/tecent.csv", "w", encoding="utf-8") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(keys)
        csv_writer.writerows(values)


def f3():
    pass


if __name__ == '__main__':
    # f1()
    f2()
