import random


def create_phone():
    # 第二位数字
    second = [3, 5, 7, 8][random.randint(0, 3)]

    # 第三位数字
    third = {
        3: random.randint(0, 9),
        4: [5, 7, 9][random.randint(0, 2)],
        5: [i for i in range(10) if i != 4][random.randint(0, 8)],
        7: [i for i in range(10) if i not in [4, 9]][random.randint(0, 7)],
        8: random.randint(0, 9),
    }[second]

    # 最后八位数字
    suffix = random.randint(9999999,100000000)

    # 拼接手机号
    return "1{}{}{}".format(second, third, suffix)

# 生成手机号
if __name__ == '__main__':
    # for i in range(100):
    phone = create_phone()
    print(phone)
